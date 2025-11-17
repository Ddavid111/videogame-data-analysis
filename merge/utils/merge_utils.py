# ======== IMPORTOK ========
import pandas as pd
import logging

from merge.utils.normalize_utils import (
    process_screenshots,
    normalize_movies_column,
    dedup_join,
    normalize_tags_column,
)
from merge.utils.clean_utils import (
    clean_html_entities,
    clean_language_field_merged,
    final_clean_language_list
)
from merge.utils.category_utils import (
    merge_developers_publishers,
    merge_categories,
    merge_tags_column,
)


def fill_missing_from_source(d: pd.DataFrame,
                             src: pd.DataFrame) -> pd.DataFrame:
    """
    Kitölti a hiányzó értékeket a d DataFrame-ben egy forrás (src) adatai
    alapján. Az appid oszlop alapján merge-öl, a közös oszlopokat balról tölti.
    """
    src = src.copy()
    src["appid"] = src["appid"].astype(str)

    common_cols = [col for col in src.columns if col in d.columns]

    merged = d.merge(
        src[common_cols],
        on="appid",
        how="left",
        suffixes=("", "_src")
    )

    for col in common_cols:
        if col != "appid":
            merged[col] = merged[col].combine_first(merged[f"{col}_src"])
            merged.drop(columns=[f"{col}_src"], inplace=True)

    return merged


def merge_sources(a: pd.DataFrame, b: pd.DataFrame, c: pd.DataFrame,
                  columns_to_merge: list[str] = None) -> pd.DataFrame:
    """
    Összefésüli az A, B, C forrásokat AppID alapján.
    C → B → A prioritással tölti ki a hiányzó adatokat.

    Paraméter:
        columns_to_merge: ha meg van adva, csak ezeket az oszlopokat
        (és appid-t) mergeli.
    """
    logging.info("Merging sources with C→B→A priority...")

    for df in [a, b, c]:
        if not df.empty:
            df["appid"] = df["appid"].astype(str).str.strip()
            df.drop_duplicates(subset="appid", inplace=True)

    if columns_to_merge:
        keep_cols = ["appid"] + [
            col
            for col in columns_to_merge
            if col in a.columns or col in b.columns or col in c.columns
        ]
        a = a[[col for col in keep_cols if col in a.columns]]
        b = b[[col for col in keep_cols if col in b.columns]]
        c = c[[col for col in keep_cols if col in c.columns]]
        logging.info(f"Using subset of columns for merge: {keep_cols}")

    columns = list(
        dict.fromkeys(
            sum(
                [df.columns.tolist() for df in [a, b, c] if not df.empty],
                [],
            )
        )
    )

    all_appids = pd.concat(
        [a[["appid"]], b[["appid"]], c[["appid"]]],
        ignore_index=True,
    ).drop_duplicates()

    d = pd.DataFrame(columns=columns)
    d["appid"] = all_appids["appid"]

    for src in [c, b, a]:
        if not src.empty:
            d = fill_missing_from_source(d, src)

    logging.info(f"Merge complete ({len(d)} rows, {len(columns)} columns)")
    return d


def finalize_sources(d, a, b, c):
    """
    Hozzáad egy 'sources' oszlopot a d (merged_master) DataFrame-hez,
    ami jelzi, hogy a sor melyik eredeti datasetből származik.
    """
    a_ids = set(a["appid"]) if not a.empty else set()
    b_ids = set(b["appid"]) if not b.empty else set()
    c_ids = set(c["appid"]) if not c.empty else set()

    sources = []
    for appid in d["appid"]:
        src = []
        if appid in c_ids:
            src.append("C")
        if appid in b_ids:
            src.append("B")
        if appid in a_ids:
            src.append("A")
        sources.append(",".join(src))

    d["sources"] = sources
    return d


def merge_and_finalize(
    a: pd.DataFrame,
    b: pd.DataFrame,
    c: pd.DataFrame,
    columns_to_merge: list[str] = None,
) -> pd.DataFrame:
    '''
    Három forrás-DataFrame (A, B, C) egyesítése és véglegesítése.

    - Merge-eli a forrásokat az `appid` alapján.
    - Kategória-, screenshot- és videóadatokat egyesít és átnevez.
    - Thumbnail és 480p videóoszlopokat hoz létre.
    - Eltávolítja a duplikált URL-eket (`dedup_join` segítségével).
    - Összevonja a fejlesztői, kiadói, kategória- és tag-információkat.
    '''
    d = merge_sources(a, b, c, columns_to_merge=columns_to_merge)

    if 'categories' in a.columns:
        d['categories_a'] = d['appid'].map(a.set_index('appid')['categories'])
    if 'categories' in b.columns:
        d['categories_b'] = d['appid'].map(b.set_index('appid')['categories'])
    if 'categories' in c.columns:
        d['categories_c'] = d['appid'].map(c.set_index('appid')['categories'])

    if "screenshots" in d.columns:
        d.rename(columns={"screenshots": "screenshots_full"}, inplace=True)
    a_thumb, b_thumb, c_thumb = process_screenshots(a, b, c)
    d["screenshots_thumb"] = d["appid"].map(
        lambda x: c_thumb.get(x, []) + b_thumb.get(x, []) + a_thumb.get(x, [])
    )

    if "movies" in d.columns:
        d.rename(columns={"movies": "movies_max"}, inplace=True)

    a_thumb_m, a_480, a_max = normalize_movies_column(a, "A")
    b_thumb_m, b_480, b_max = normalize_movies_column(b, "B")
    c_thumb_m, c_480, c_max = normalize_movies_column(c, "C")

    d["movies_thumbnail"] = d["appid"].map(
        lambda x: c_thumb_m.get(x, [])
        + b_thumb_m.get(x, [])
        + a_thumb_m.get(x, [])
    )
    d["movies_480"] = d["appid"].map(
        lambda x: c_480.get(x, [])
        + b_480.get(x, [])
        + a_480.get(x, [])
    )

    for col in ["screenshots_thumb", "movies_thumbnail", "movies_480"]:
        d[col] = d[col].apply(dedup_join)

    d = finalize_sources(d, a, b, c)

    d = merge_developers_publishers(d)
    d = merge_categories(d)

    tags_df = merge_tags_column(d, a, b, c)

    tags_collapsed = (
        tags_df.groupby("appid")
        .apply(
            lambda x: [
                {"tag_name": t, "weight": w}
                for t, w in zip(x["tag_name"], x["weight"])
            ]
        )
        .reset_index(name="tags")
    )

    d = d.merge(tags_collapsed, on="appid", how="left")

    for col in ["detailed_description", "about_the_game", "short_description"]:
        if col in d.columns:
            d[col] = d[col].astype(str).apply(clean_html_entities)

    if "owners" in d.columns and "estimated_owners" in d.columns:
        d["estimated_owners"] = d["estimated_owners"].combine_first(
            d["owners"]
        )
        d.drop(columns=["owners"], inplace=True)
    elif "owners" in d.columns:
        d.rename(columns={"owners": "estimated_owners"}, inplace=True)

    if "positive" in d.columns and "positive_ratings" in d.columns:
        d["positive"] = d["positive"].combine_first(d["positive_ratings"])
        d.drop(columns=["positive_ratings"], inplace=True)
    elif "positive_ratings" in d.columns:
        d.rename(columns={"positive_ratings": "positive"}, inplace=True)

    if "negative" in d.columns and "negative_ratings" in d.columns:
        d["negative"] = d["negative"].combine_first(d["negative_ratings"])
        d.drop(columns=["negative_ratings"], inplace=True)
    elif "negative_ratings" in d.columns:
        d.rename(columns={"negative_ratings": "negative"}, inplace=True)

    if (
        "average_playtime" in d.columns
        and "average_playtime_forever" in d.columns
    ):
        d["average_playtime_forever"] = (
            d["average_playtime_forever"].combine_first(
                d["average_playtime"]
            )
        )
        d.drop(columns=["average_playtime"], inplace=True)
    elif "average_playtime" in d.columns:
        d.rename(
            columns={"average_playtime": "average_playtime_forever"},
            inplace=True,
        )

    if (
        "median_playtime" in d.columns
        and "median_playtime_forever" in d.columns
    ):
        d["median_playtime_forever"] = (
            d["median_playtime_forever"]
            .combine_first(d["median_playtime"])
        )
        d.drop(columns=["median_playtime"], inplace=True)
    elif "median_playtime" in d.columns:
        d.rename(
            columns={"median_playtime": "median_playtime_forever"},
            inplace=True,
        )

    tag_cols = [c for c in d.columns if c.startswith("tags")]

    if len(tag_cols) > 1:
        d["tags"] = d[tag_cols].bfill(axis=1).iloc[:, 0]
        for c in tag_cols:
            if c != "tags":
                d.drop(columns=c, inplace=True, errors="ignore")
        logging.info(
            f"Combined duplicate tag columns: {tag_cols} → kept unified 'tags'"
        )

    if "tags" in d.columns:
        d["tags"] = d["tags"].apply(normalize_tags_column)

    for col in d.columns:
        if "steamspy" in col.lower() and "tag" in col.lower():
            d.drop(columns=[col], inplace=True, errors="ignore")
            logging.info(f"Dropped redundant column: {col}")

    for col in ["supported_languages", "full_audio_languages"]:
        if col in d.columns:
            d[col] = d[col].apply(clean_language_field_merged)
            logging.info(f"Cleaned and normalized language field: {col}")

    for col in ["supported_languages", "full_audio_languages"]:
        if col in d.columns:
            before_counts = d[col].apply(len).sum()
            d[col] = d[col].apply(final_clean_language_list)
            after_counts = d[col].apply(len).sum()
            logging.info(
                "Final language cleanup on %s: %s → %s entries (after "
                "filtering).",
                col,
                before_counts,
                after_counts,
            )

    if ("supported_languages" in d.columns
            and "full_audio_languages" in d.columns):
        identical_rows = (
            d["supported_languages"].astype(str)
            == d["full_audio_languages"].astype(str)
        ).sum()
        logging.info(
            "%s rows have identical supported and audio "
            "language sets.",
            identical_rows,
        )

    return d
