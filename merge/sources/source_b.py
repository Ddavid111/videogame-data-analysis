#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# ======== IMPORTOK ========
import os
import json
import pandas as pd
import logging
from typing import Any


# ======== SOURCE B LOADING ========
def load_source_b(base_path: str) -> pd.DataFrame:
    """
    Betölti a B forrást JSON fájlból, előkészíti Pandas DataFrame-re,
    és beállítja a numerikus és logikai oszlopok típusait.
    """
    file_path = os.path.join(base_path, "games.json")

    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return pd.DataFrame()

    with open(file_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    records = []
    for appID, game in dataset.items():
        fields = [
            "name",
            "release_date",
            "estimated_owners",
            "price",
            "required_age",
            "dlc_count",
            "detailed_description",
            "short_description",
            "about_the_game",
            "reviews",
            "header_image",
            "website",
            "support_url",
            "support_email",
            "windows",
            "mac",
            "linux",
            "metacritic_score",
            "metacritic_url",
            "user_score",
            "positive",
            "negative",
            "score_rank",
            "achievements",
            "recommendations",
            "notes",
            "average_playtime_forever",
            "average_playtime_2weeks",
            "median_playtime_forever",
            "median_playtime_2weeks",
            "peak_ccu",
        ]

        record = {key: game.get(key) for key in fields}
        record["appid"] = str(appID)

        list_fields = [
            "packages", "developers", "publishers", "categories", "genres",
            "supported_languages", "full_audio_languages", "screenshots", "movies"
        ]
        record.update({f: game.get(f, []) for f in list_fields})

        tags = game.get("tags", {})
        record["tags"] = tags if isinstance(tags, dict) else {}


        records.append(record)

    df_b = pd.DataFrame(records)

    if "release_date" in df_b.columns:
        df_b["release_date"] = pd.to_datetime(df_b["release_date"], errors="coerce")
        df_b["release_date"] = df_b["release_date"].dt.strftime("%Y-%m-%d")
        df_b["release_date"] = df_b["release_date"].replace("NaT", None)

    df_b_exploded = df_b.explode("packages").dropna(subset=["packages"])

    numeric_cols = [
        "metacritic_score",
        "user_score",
        "positive",
        "negative",
        "achievements",
        "recommendations",
        "price",
        "required_age",
        "dlc_count",
        "average_playtime_forever",
        "average_playtime_2weeks",
        "median_playtime_forever",
        "median_playtime_2weeks",
        "peak_ccu",
    ]

    packages_df = pd.json_normalize(df_b.explode("packages")["packages"])

    for col in numeric_cols:
        if col in df_b.columns:
            df_b[col] = pd.to_numeric(df_b[col], errors="coerce")

    bool_cols = ["windows", "mac", "linux"]
    for col in bool_cols:
        if col in df_b.columns:
            df_b[col] = df_b[col].astype(bool)

    logging.info(f"B source loaded from JSON: {len(df_b)} rows")
    return df_b

