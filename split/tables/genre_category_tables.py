#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd
import logging

def create_genres_table(master_df: pd.DataFrame, output_dir: str = None):
    """
    Létrehozza a game_genre és genres táblákat:
    - game_genre: appid + genreid
    - genres: genreid + genre_name (eredeti genres mező)
    """
    rows = []

    for _, row in master_df.iterrows():
        appid = row["appid"]
        genres_raw = row.get("genres", "")

        text = str(genres_raw).strip()
        if text in ["", "[]", "['']"]:
            continue

        rows.append({"appid": appid, "genre_name": text})

    df_flat = pd.DataFrame(rows).drop_duplicates().reset_index(drop=True)

    df_flat.insert(1, "genreid", range(1, len(df_flat)+1))

    game_genre_df = df_flat[['appid', 'genreid']].copy()
    genres_df = df_flat[['genreid', 'genre_name']].copy()

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        genres_path = os.path.join(output_dir, "genres.csv")
        game_genre_path = os.path.join(output_dir, "game_genre.csv")
        genres_df.to_csv(genres_path, index=False)
        game_genre_df.to_csv(game_genre_path, index=False)
        logging.info(f"Saved 'genres.csv' ({len(genres_df)} rows) to {output_dir}")
        logging.info(f"Saved 'game_genre.csv' ({len(game_genre_df)} rows) to {output_dir}")

    return genres_df, game_genre_df

def create_categories_table(master_df: pd.DataFrame, output_dir: str = None):
    """
    Létrehozza a game_category és categories táblákat:
    - game_category: appid + catid
    - categories: catid + name (eredeti categories mező)
    """
    rows = []

    for _, row in master_df.iterrows():
        appid = row["appid"]
        categories_raw = row.get("categories", "")

        text = str(categories_raw).strip()
        if text in ["", "[]", "['']"]:
            continue

        rows.append({"appid": appid, "name": text})

    df_flat = pd.DataFrame(rows).drop_duplicates().reset_index(drop=True)

    df_flat.insert(1, "catid", range(1, len(df_flat)+1))

    game_category_df = df_flat[['appid', 'catid']].copy()
    categories_df = df_flat[['catid', 'name']].copy()

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        categories_path = os.path.join(output_dir, "categories.csv")
        game_category_path = os.path.join(output_dir, "game_category.csv")
        categories_df.to_csv(categories_path, index=False)
        game_category_df.to_csv(game_category_path, index=False)
        logging.info(f"Saved 'categories.csv' ({len(categories_df)} rows) to {output_dir}")
        logging.info(f"Saved 'game_category.csv' ({len(game_category_df)} rows) to {output_dir}")

    return categories_df, game_category_df

