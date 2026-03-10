# ======== IMPORTOK ========
import ast
import numpy as np
import pandas as pd
from merge.utils.normalize_utils import flatten_values


# ======== DEVELOPER / PUBLISHER MERGE ========
def combine_cols(row: pd.Series, cols: list[str]) -> str:
    """
    Több oszlopból származó értékeket kombinál egyetlen,
    duplikátummentes stringgé.

    - Kinyeri az értékeket a megadott oszlopokból.
    - Támogatja a listákat, NumPy tömböket és skalárokat is.
    - A duplikátumokat eltávolítja és vesszővel elválasztva adja vissza.
    """
    vals = []
    for col in cols:
        val = row.get(col, None)
        if val is None:
            continue
        if isinstance(val, (list, np.ndarray)):
            vals.extend(flatten_values(val))
        else:
            vals.extend(flatten_values([val]))
    return ", ".join(list(dict.fromkeys(vals)))


def merge_developers_publishers(d: pd.DataFrame) -> pd.DataFrame:
    """
    Összevonja a fejlesztői és kiadói oszlopokat, eltávolítva a duplikált
    neveket.

    - A 'developer' és 'developers' oszlopokból egyesített 'developers'
      oszlopot hoz létre.
    - A 'publisher' és 'publishers' oszlopokból egyesített 'publishers'
      oszlopot hoz létre.
    - Az eredeti ('developer', 'publisher') oszlopokat eltávolítja.
    """
    d["developers"] = d.apply(
        lambda row: combine_cols(row, ["developer", "developers"]),
        axis=1,
    )
    d["publishers"] = d.apply(
        lambda row: combine_cols(row, ["publisher", "publishers"]),
        axis=1,
    )

    for col in ["developer", "publisher"]:
        if col in d.columns:
            d.drop(columns=[col], inplace=True)

    return d


# ======== CATEGORY MERGE ========
def parse_categories(val) -> list[str]:
    """
    Kategóriaértékek egységes listává alakítása.

    - Kezeli a listákat, NumPy tömböket, stringeket és None értékeket.
    - Tisztítja az üres vagy NaN értékeket.
    - Felismeri a stringként tárolt listákat és a pontosvesszővel tagolt
      formátumokat.
    """
    if val is None:
        return []
    if isinstance(val, (float, np.floating)) and np.isnan(val):
        return []
    if isinstance(val, (list, np.ndarray)):
        return [
            str(v).strip()
            for v in val
            if isinstance(v, str) and v.strip()
        ]
    if isinstance(val, str):
        val = val.strip()
        if not val:
            return []
        if val.startswith("[") and val.endswith("]"):
            try:
                parsed = ast.literal_eval(val)
                if isinstance(parsed, list):
                    return [str(v).strip() for v in parsed
                            if isinstance(v, str) and v.strip()]
            except Exception:
                pass
        if ";" in val:
            return [v.strip() for v in val.split(";") if v.strip()]
        return [val]
    return []


def combine_categories(row: pd.Series) -> str:
    """
    Egy sor kategóriaoszlopait (A, B, C) kombinálja egyetlen, duplikátummentes
    stringgé.
    """
    cats_a = parse_categories(
        row.get("categories_a", row.get("categories", None))
    )
    cats_b = parse_categories(row.get("categories_b", None))
    cats_c = parse_categories(row.get("categories_c", None))

    merged = []
    seen_lower = set()

    for c in cats_a + cats_b + cats_c:
        cl = c.lower()
        if cl not in seen_lower:
            merged.append(c)
            seen_lower.add(cl)

    return ", ".join(merged)


def merge_categories(d: pd.DataFrame) -> pd.DataFrame:
    """
    A források kategóriaoszlopait egyesíti egységes 'categories' oszlopba.

    - A 'categories_a', 'categories_b', 'categories_c' oszlopokat kombinálja.
    - Duplikátumokat kiszűri, kisbetű-érzéketlen módon.
    - Eltávolítja a felesleges kategóriaoszlopokat.
    """
    category_cols = [c for c in d.columns if "categor" in c.lower()]
    d["categories"] = d.apply(combine_categories, axis=1)

    for col in category_cols:
        if col != "categories":
            d.drop(columns=[col], inplace=True, errors="ignore")

    return d


# ======== TAG MERGE ========
def merge_tags_column(d: pd.DataFrame, a: pd.DataFrame, b: pd.DataFrame,
                      c: pd.DataFrame) -> pd.DataFrame:
    """
    Egyesíti a címkék (tags) adatokat az A, B, C forrásokból AppID alapján.

    - Az A forrásban a tags stringként tárolt, vesszővel elválasztott lista.
    - A B forrásban a tags dict formátumú (név → súly).
    - A C forrásban vegyes formátumot kezel (stringként tárolt dict is lehet).
    - Az eredmény egy DataFrame, ami appid, tag_name, weight oszlopokat
      tartalmaz.
    """
    tags_a_dict = {}
    if 'tags' in a.columns:
        for appid, tags_str in zip(a['appid'], a['tags']):
            if isinstance(tags_str, str):
                tags_list = [
                    t.strip()
                    for t in tags_str.split(",")
                    if t.strip()
                ]
                tags_a_dict[str(appid)] = {t: 1 for t in tags_list}

    tags_b_dict = {}
    if 'tags' in b.columns:
        for appid, tags_json in zip(b['appid'], b['tags']):
            if isinstance(tags_json, dict):
                tags_b_dict[str(appid)] = tags_json

    tags_c_dict = {}
    if 'tags' in c.columns:
        for appid, tags_str in zip(c['appid'], c['tags']):
            if isinstance(tags_str, str):
                try:
                    tags_dict = ast.literal_eval(tags_str)
                    if isinstance(tags_dict, dict):
                        tags_c_dict[str(appid)] = tags_dict
                except (ValueError, SyntaxError):
                    continue
    tag_rows = []
    for appid in d['appid']:
        tag_dict = {}
        tag_dict.update(tags_a_dict.get(str(appid), {}))
        tag_dict.update(tags_b_dict.get(str(appid), {}))
        tag_dict.update(tags_c_dict.get(str(appid), {}))

        for t, w in tag_dict.items():
            tag_rows.append({"appid": appid, "tag_name": t, "weight": w})

    tags_df = pd.DataFrame(tag_rows)
    return tags_df
