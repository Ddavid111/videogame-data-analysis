#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

def fill_missing_from_source(D: pd.DataFrame, src: pd.DataFrame) -> pd.DataFrame:
    """
    Kitölti a hiányzó értékeket a D DataFrame-ben egy forrás (src) adatai alapján.
    Az appid oszlop alapján merge-öl, a közös oszlopokat balról tölti.
    """
    src = src.copy()
    src["appid"] = src["appid"].astype(str)

    common_cols = [col for col in src.columns if col in D.columns]

    merged = D.merge(
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

def merge_sources(a: pd.DataFrame, b: pd.DataFrame, c: pd.DataFrame, columns_to_merge: list[str] = None) -> pd.DataFrame:
    """
    Összefésüli az A, B, C forrásokat AppID alapján.
    C → B → A prioritással tölti ki a hiányzó adatokat.

    Paraméter:
        columns_to_merge: ha meg van adva, csak ezeket az oszlopokat (és appid-t) mergeli.
    """
    logging.info("Merging sources with C→B→A priority...")

    for df in [a, b, c]:
        if not df.empty:
            df["appid"] = df["appid"].astype(str).str.strip()
            df.drop_duplicates(subset="appid", inplace=True)

    if columns_to_merge:
        keep_cols = ["appid"] + [col for col in columns_to_merge if col in a.columns or col in b.columns or col in c.columns]
        a = a[[col for col in keep_cols if col in a.columns]]
        b = b[[col for col in keep_cols if col in b.columns]]
        c = c[[col for col in keep_cols if col in c.columns]]
        logging.info(f"Using subset of columns for merge: {keep_cols}")

    columns = list(dict.fromkeys(
        sum([df.columns.tolist() for df in [a, b, c] if not df.empty], [])
    ))

    all_appids = pd.concat([a[["appid"]], b[["appid"]], c[["appid"]]], ignore_index=True).drop_duplicates()

    D = pd.DataFrame(columns=columns)
    D["appid"] = all_appids["appid"]

    for src in [c, b, a]:
        if not src.empty:
            D = fill_missing_from_source(D, src)

    logging.info(f"Merge complete ({len(D)} rows, {len(columns)} columns)")
    return D

def finalize_sources(D, a, b, c):
    """
    Hozzáad egy 'sources' oszlopot a D (merged_master) DataFrame-hez,
    ami jelzi, hogy a sor melyik eredeti datasetből származik.
    """
    a_ids = set(a["appid"]) if not a.empty else set()
    b_ids = set(b["appid"]) if not b.empty else set()
    c_ids = set(c["appid"]) if not c.empty else set()

    sources = []
    for appid in D["appid"]:
        src = []
        if appid in c_ids:
            src.append("C")
        if appid in b_ids:
            src.append("B")
        if appid in a_ids:
            src.append("A")
        sources.append(",".join(src))

    D["sources"] = sources
    return D

def merge_and_finalize(a: pd.DataFrame, b: pd.DataFrame, c: pd.DataFrame, columns_to_merge: list[str] = None) -> pd.DataFrame:
    '''
    Három forrás-DataFrame (A, B, C) egyesítése és véglegesítése.

    - Merge-eli a forrásokat az `appid` alapján.
    - Kategória-, screenshot- és videóadatokat egyesít és átnevez.
    - Thumbnail és 480p videóoszlopokat hoz létre.
    - Eltávolítja a duplikált URL-eket (`dedup_join` segítségével).
    - Összevonja a fejlesztői, kiadói, kategória- és tag-információkat.
    '''
    D = merge_sources(a, b, c, columns_to_merge=columns_to_merge)

    if 'categories' in a.columns:
        D['categories_a'] = D['appid'].map(a.set_index('appid')['categories'])
    if 'categories' in b.columns:
        D['categories_b'] = D['appid'].map(b.set_index('appid')['categories'])
    if 'categories' in c.columns:
        D['categories_c'] = D['appid'].map(c.set_index('appid')['categories'])

    if "screenshots" in D.columns:
        D.rename(columns={"screenshots": "screenshots_full"}, inplace=True)
    a_thumb, b_thumb, c_thumb = process_screenshots(a, b, c)
    D["screenshots_thumb"] = D["appid"].map(
        lambda x: c_thumb.get(x, []) + b_thumb.get(x, []) + a_thumb.get(x, [])
    )

    if "movies" in D.columns:
        D.rename(columns={"movies": "movies_max"}, inplace=True)

    a_thumb_m, a_480, a_max = normalize_movies_column(a, "A")
    b_thumb_m, b_480, b_max = normalize_movies_column(b, "B")
    c_thumb_m, c_480, c_max = normalize_movies_column(c, "C")

    D["movies_thumbnail"] = D["appid"].map(lambda x: c_thumb_m.get(x, []) + b_thumb_m.get(x, []) + a_thumb_m.get(x, []))
    D["movies_480"] = D["appid"].map(lambda x: c_480.get(x, []) + b_480.get(x, []) + a_480.get(x, []))


    for col in ["screenshots_thumb", "movies_thumbnail", "movies_480"]:
        D[col] = D[col].apply(dedup_join)

    D = finalize_sources(D, a, b, c)

    D = merge_developers_publishers(D)
    D = merge_categories(D)

    tags_df = merge_tags_column(D, a, b, c)

    tags_collapsed = (
        tags_df.groupby("appid")
        .apply(lambda x: [{"tag_name": t, "weight": w} for t, w in zip(x["tag_name"], x["weight"])])
        .reset_index(name="tags")
    )

    D = D.merge(tags_collapsed, on="appid", how="left")

    for col in ["detailed_description", "about_the_game", "short_description"]:
        if col in D.columns:
            D[col] = D[col].astype(str).apply(clean_html_entities)

    if "owners" in D.columns and "estimated_owners" in D.columns:
        D["estimated_owners"] = D["estimated_owners"].combine_first(D["owners"])
        D.drop(columns=["owners"], inplace=True)
    elif "owners" in D.columns:
        D.rename(columns={"owners": "estimated_owners"}, inplace=True)

    if "positive" in D.columns and "positive_ratings" in D.columns:
        D["positive"] = D["positive"].combine_first(D["positive_ratings"])
        D.drop(columns=["positive_ratings"], inplace=True)
    elif "positive_ratings" in D.columns:
        D.rename(columns={"positive_ratings": "positive"}, inplace=True)

    if "negative" in D.columns and "negative_ratings" in D.columns:
        D["negative"] = D["negative"].combine_first(D["negative_ratings"])
        D.drop(columns=["negative_ratings"], inplace=True)
    elif "negative_ratings" in D.columns:
        D.rename(columns={"negative_ratings": "negative"}, inplace=True)

    if "average_playtime" in D.columns and "average_playtime_forever" in D.columns:
        D["average_playtime_forever"] = D["average_playtime_forever"].combine_first(D["average_playtime"])
        D.drop(columns=["average_playtime"], inplace=True)
    elif "average_playtime" in D.columns:
        D.rename(columns={"average_playtime": "average_playtime_forever"}, inplace=True)

    if "median_playtime" in D.columns and "median_playtime_forever" in D.columns:
        D["median_playtime_forever"] = D["median_playtime_forever"].combine_first(D["median_playtime"])
        D.drop(columns=["median_playtime"], inplace=True)
    elif "median_playtime" in D.columns:
        D.rename(columns={"median_playtime": "median_playtime_forever"}, inplace=True)

    tag_cols = [c for c in D.columns if c.startswith("tags")]

    if len(tag_cols) > 1:
        D["tags"] = D[tag_cols].bfill(axis=1).iloc[:, 0]
        for c in tag_cols:
            if c != "tags":
                D.drop(columns=c, inplace=True, errors="ignore")
        logging.info(f"Combined duplicate tag columns: {tag_cols} → kept unified 'tags'")

    if "tags" in D.columns:
        D["tags"] = D["tags"].apply(normalize_tags_column)

    for col in D.columns:
        if "steamspy" in col.lower() and "tag" in col.lower():
            D.drop(columns=[col], inplace=True, errors="ignore")
            logging.info(f"Dropped redundant column: {col}")

    for col in ["supported_languages", "full_audio_languages"]:
        if col in D.columns:
            D[col] = D[col].apply(clean_language_field_merged)
            logging.info(f"Cleaned and normalized language field: {col}")

            
    for col in ["supported_languages", "full_audio_languages"]:
        if col in D.columns:
            before_counts = D[col].apply(len).sum()
            D[col] = D[col].apply(final_clean_language_list)
            after_counts = D[col].apply(len).sum()
            logging.info(
                f"Final language cleanup on {col}: {before_counts} → {after_counts} entries (after filtering)."
            )

    if "supported_languages" in D.columns and "full_audio_languages" in D.columns:
        identical_rows = (D["supported_languages"].astype(str) == D["full_audio_languages"].astype(str)).sum()
        logging.info(f"{identical_rows} rows have identical supported and audio language sets.")

    return D

