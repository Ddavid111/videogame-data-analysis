import os
import pandas as pd
import logging
from utils.text_utils import join_urls


def create_media_table(master_df: pd.DataFrame,
                       output_dir: str = None) -> pd.DataFrame:
    """
    Létrehozza a media táblát a merged_master-ből.

    """
    media_cols = ["appid", "header_image", "background"]
    media_df = master_df[
        [c for c in media_cols if c in master_df.columns]
    ].copy()

    media_df = media_df.dropna(subset=["header_image"]).reset_index(drop=True)

    media_df.insert(0, "mediaid", range(1, len(media_df)+1))

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "media.csv")
        media_df.to_csv(path, index=False)
        logging.info(
            f"Saved 'media.csv' ({len(media_df)} rows) to {output_dir}"
        )

    return media_df


def create_screenshots_table(master_df: pd.DataFrame,
                             output_dir: str = None) -> pd.DataFrame:
    """
    Létrehozza a screenshots táblát a master DataFrame-ből.

    - Kiválasztja az 'appid', 'screenshots_full' és
      'screenshots_thumb' oszlopokat.
    - A listákat stringgé alakítja (`join_urls` segítségével).
    - Eltávolítja az üres sorokat.
    - Hozzáad egy automatikus 'screenshotid' azonosítót.
    - CSV-fájlba menti az eredményt.
    """
    cols = ["appid"]
    for c in ["screenshots_full", "screenshots_thumb"]:
        if c in master_df.columns:
            cols.append(c)

    df = master_df[cols].copy()

    for c in ["screenshots_full", "screenshots_thumb"]:
        if c in df.columns:
            df[c] = df[c].apply(join_urls)

    df = df[
        (df.get("screenshots_full", "") != "") |
        (df.get("screenshots_thumb", "") != "")
    ].reset_index(drop=True)

    df.insert(0, "screenshotid", range(1, len(df) + 1))

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "screenshots.csv")
        df.to_csv(path, index=False)
        logging.info(
            f"Saved 'screenshots.csv' ({len(df)} rows) to {output_dir}"
        )

    return df


def create_movies_table(master_df: pd.DataFrame,
                        output_dir: str = None) -> pd.DataFrame:
    """
    Létrehozza a 'movies' táblát a master DataFrame-ből.

    - Kiválasztja az 'appid', 'movies_thumbnail', 'movies_max' és
      'movies_480' oszlopokat.
    - A listákat stringgé alakítja (`join_urls` segítségével).
    - Csak azokat a sorokat tartja meg, ahol legalább egy URL szerepel.
    - Hozzáad egy automatikus 'movieid' azonosítót.
    - (Opcionálisan) CSV-fájlba menti az eredményt.

    Visszatér: a videókat tartalmazó DataFrame.
    """
    cols = ["appid"]
    for c in ["movies_thumbnail", "movies_max", "movies_480"]:
        if c in master_df.columns:
            cols.append(c)

    df = master_df[cols].copy()

    for c in ["movies_thumbnail", "movies_max", "movies_480"]:
        if c in df.columns:
            df[c] = df[c].apply(join_urls)

    df = df[
        (df.get("movies_thumbnail", "") != "") |
        (df.get("movies_max", "") != "") |
        (df.get("movies_480", "") != "")
    ].reset_index(drop=True)

    df.insert(0, "movieid", range(1, len(df) + 1))

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "movies.csv")
        df.to_csv(path, index=False)
        logging.info(f"Saved 'movies.csv' ({len(df)} rows) to {output_dir}")

    return df
