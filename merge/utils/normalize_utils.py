# ======== IMPORTOK ========
import ast
import numpy as np
import pandas as pd
import logging


# ======== NORMALIZATION FUNCTIONS ========
def normalize_tags_column(val):
    """
    Egységesíti a 'tags' oszlop értékeit:
    - Ha dict-string: {'Action': 5472, 'FPS': 4897}
      → [{"tag_name": "Action", "weight": 5472}, ...]
    - Ha már list-of-dict, érintetlenül hagyja.
    """
    if isinstance(val, str):
        try:
            parsed = ast.literal_eval(val)
            if isinstance(parsed, dict):
                return [
                    {"tag_name": k, "weight": v}
                    for k, v in parsed.items()
                ]
        except Exception:
            pass
    return val


def normalize_screenshots_column(df: pd.DataFrame, source_name: str):
    """
    Kivonatolja a screenshots oszlopot (ha létezik) és visszaadja a thumbnail
    URL-eket. Működik dict/list/str típusokra is.
    """
    thumb_dict = {}

    if "screenshots" not in df.columns:
        return thumb_dict

    for appid, val in df[["appid", "screenshots"]].itertuples(index=False):
        thumb_urls = []

        if val is None:
            continue
        if isinstance(val, float) and np.isnan(val):
            continue

        try:
            data = ast.literal_eval(val) if isinstance(val, str) else val
        except Exception:
            continue

        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    thumb = item.get("path_thumbnail") or item.get("thumb")
                    if thumb:
                        thumb_urls.append(thumb.strip())
                elif isinstance(item, str):
                    pass

        thumb_urls = [
            u for u in thumb_urls
            if isinstance(u, str) and u.startswith("http")
        ]
        thumb_urls = list(dict.fromkeys(thumb_urls))

        thumb_dict[str(appid)] = thumb_urls

    logging.info(
        f"Normalized thumbnail screenshots for source {source_name} "
        f"({len(thumb_dict)} items)"
    )
    return thumb_dict


def process_screenshots(a, b, c):
    """
    Normalizálja a screenshots oszlopokat,
    visszaadja a thumbnail dict-eket.
    """
    a_thumb = normalize_screenshots_column(a, "A")
    b_thumb = normalize_screenshots_column(b, "B")
    c_thumb = normalize_screenshots_column(c, "C")
    return a_thumb, b_thumb, c_thumb


def normalize_movies_column(df: pd.DataFrame, source_name: str):
    '''
    Normalizálja a 'movies' oszlopot:
    - movies_thumbnail: a 'thumbnail' URL-ek
    - movies_480: a 'webm.480' URL-ek
    - movies_max: a 'webm.max' URL-ek
    '''
    thumb_dict = {}
    m480_dict = {}
    mmax_dict = {}

    if "movies" not in df.columns:
        return thumb_dict, m480_dict, mmax_dict

    for appid, val in df[["appid", "movies"]].itertuples(index=False):
        thumbs = []
        webm_480 = []
        webm_max = []

        if val is None:
            continue
        if isinstance(val, float) and np.isnan(val):
            continue

        try:
            data = ast.literal_eval(val) if isinstance(val, str) else val
        except Exception:
            continue

        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    t = item.get("thumbnail")
                    if t:
                        thumbs.append(t.strip())
                    w480 = item.get("webm", {}).get("480")
                    if w480:
                        webm_480.append(w480.strip())
                    wmax = item.get("webm", {}).get("max")
                    if wmax:
                        webm_max.append(wmax.strip())

        thumb_dict[str(appid)] = thumbs
        m480_dict[str(appid)] = webm_480
        mmax_dict[str(appid)] = (
            mmax_dict.get(str(appid), []) + mmax_dict.get(str(appid), [])
        )

    logging.info(
        f"Normalized movies for source {source_name} "
        f"({len(thumb_dict)} items)"
    )
    return thumb_dict, m480_dict, mmax_dict


def dedup_join(urls):
    '''
    Egy lista vagy tuple URL-t megtisztít duplikátumoktól és
    vesszővel összefűzi őket.
    '''
    if not urls or not isinstance(urls, (list, tuple)):
        return ""
    return ", ".join(list(dict.fromkeys(urls)))


def flatten_values(vals):
    """Lapítja a listákat / stringként tárolt listákat egy sima listává."""
    flat = []
    for v in vals:
        if isinstance(v, str):
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                try:
                    sublist = ast.literal_eval(v)
                    if isinstance(sublist, list):
                        flat.extend(
                            [str(s).strip() for s in sublist if pd.notna(s)]
                        )
                        continue
                except Exception:
                    pass
        flat.append(str(v).strip())
    return list(dict.fromkeys(flat))
