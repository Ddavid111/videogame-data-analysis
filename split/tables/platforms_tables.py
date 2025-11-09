#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd
import logging

def create_platforms_table(master_df: pd.DataFrame, output_dir: str = None):
    """
    Létrehozza a game_platform és platforms táblákat:
    - game_platform: appid + platid
    - platforms: platid + windows/linux/mac logikai mezők
    """
    rows = []

    for _, row in master_df.iterrows():
        appid = row["appid"]
        windows = bool(row.get("windows", False))
        linux = bool(row.get("linux", False))
        mac = bool(row.get("mac", False))

        rows.append({
            "appid": appid,
            "windows": windows,
            "linux": linux,
            "mac": mac
        })

    df_flat = pd.DataFrame(rows).drop_duplicates().reset_index(drop=True)

    df_flat.insert(1, "platid", range(1, len(df_flat)+1))

    game_platform_df = df_flat[['appid', 'platid']].copy()
    platforms_df = df_flat[['platid', 'windows', 'linux', 'mac']].copy()

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        platforms_path = os.path.join(output_dir, "platforms.csv")
        game_platform_path = os.path.join(output_dir, "game_platform.csv")
        platforms_df.to_csv(platforms_path, index=False)
        game_platform_df.to_csv(game_platform_path, index=False)
        logging.info(f"Saved 'platforms.csv' ({len(platforms_df)} rows) to {output_dir}")
        logging.info(f"Saved 'game_platform.csv' ({len(game_platform_df)} rows) to {output_dir}")

    return platforms_df, game_platform_df

