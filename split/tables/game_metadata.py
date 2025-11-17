import os
import pandas as pd
import logging


def create_description_table(master_df: pd.DataFrame,
                             output_dir: str = None) -> pd.DataFrame:
    """
    Létrehozza a 'description' táblát a master DataFrame-ből.

    Tartalmazza:
      - descriptionid (1-től generált)
      - appid
      - detailed_description
      - about_the_game
      - short_description
    """
    cols = [
        "appid",
        "detailed_description",
        "about_the_game",
        "short_description",
    ]
    existing_cols = [c for c in cols if c in master_df.columns]

    if not existing_cols:
        logging.warning("No description columns found in master dataframe.")
        return pd.DataFrame()

    df = master_df[existing_cols].copy()

    df = df[
        (df.get("detailed_description", "") != "") |
        (df.get("about_the_game", "") != "") |
        (df.get("short_description", "") != "")
    ].reset_index(drop=True)

    df.insert(0, "descriptionid", range(1, len(df) + 1))

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "description.csv")
        df.to_csv(path, index=False)
        logging.info(
            f"Saved 'description.csv' ({len(df)} rows) to {output_dir}"
        )

    return df


def create_game_table(master_df: pd.DataFrame,
                      output_dir: str = None) -> pd.DataFrame:
    """
    Létrehozza a 'game.csv' táblát a master DataFrame-ből.
    Csak az appid, name és release_date mezőket tartalmazza.
    Nem szűri ki az üres neveket.
    """
    cols = [
        "appid", "name", "release_date", "estimated_owners", "required_age",
        "price", "dlc_count", "recommendations", "notes", "website",
        "metacritic_score", "metacritic_url", "achievements", "user_score",
        "score_rank", "positive", "negative", "average_playtime_forever",
        "average_playtime_2weeks", "median_playtime_forever",
        "median_playtime_2weeks", "peak_ccu", "discount", "pct_pos_total",
        "pct_pos_recent", "num_reviews_total", "num_reviews_recent",
        "reviews", "english",
    ]
    existing_cols = [c for c in cols if c in master_df.columns]

    if "appid" not in existing_cols:
        logging.warning("Missing 'appid' column in master dataframe.")
        return pd.DataFrame()

    df = master_df[existing_cols].copy()

    df = df.reset_index(drop=True)

    if "recommendations" in df.columns:
        df.rename(
            columns={"recommendations": "num_recommendations"},
            inplace=True,
        )

    if "achievements" in df.columns:
        df.rename(columns={"achievements": "num_achievements"}, inplace=True)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "game.csv")
        df.to_csv(path, index=False, encoding="utf-8-sig")
        logging.info(f"Saved 'game.csv' ({len(df)} rows) to {output_dir}")

    return df
