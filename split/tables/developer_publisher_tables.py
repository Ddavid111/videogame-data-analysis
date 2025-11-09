#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd
import logging

def create_developer_tables(master_df: pd.DataFrame, output_dir: str = None):
    """
    Létrehozza a developers és game_developer táblákat úgy,
    hogy minden játékhoz egy sor tartozik, még ha több fejlesztője is van.
    - game_developer: appid + devid (1-től generált)
    - developers: devid + name (összefűzött fejlesztők)
    """
    rows = []

    for _, row in master_df.iterrows():
        appid = row["appid"]
        devs_raw = row.get("developers", "")
        if not devs_raw or pd.isna(devs_raw):
            continue

        if isinstance(devs_raw, list):
            dev_list = [str(d).strip() for d in devs_raw if str(d).strip()]
        else:
            dev_list = [d.strip() for d in str(devs_raw).split(",") if d.strip()]

        if not dev_list:
            continue

        combined_devs = ", ".join(dev_list)
        rows.append({"appid": appid, "developer_name": combined_devs})

    df_flat = pd.DataFrame(rows).reset_index(drop=True)

    df_flat.insert(1, "devid", range(1, len(df_flat)+1))

    game_developer_df = df_flat[['appid', 'devid']].copy()
    developers_df = df_flat[['devid', 'developer_name']].copy()

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        developers_path = os.path.join(output_dir, "developers.csv")
        game_developer_path = os.path.join(output_dir, "game_developer.csv")
        developers_df.to_csv(developers_path, index=False)
        game_developer_df.to_csv(game_developer_path, index=False)
        logging.info(f"Saved 'developers.csv' ({len(developers_df)} rows) to {output_dir}")
        logging.info(f"Saved 'game_developer.csv' ({len(game_developer_df)} rows) to {output_dir}")

    return developers_df, game_developer_df

def create_publisher_tables(master_df: pd.DataFrame, output_dir: str = None):
    """
    Létrehozza a publishers és game_publisher táblákat úgy,
    hogy minden játékhoz egy sor tartozik, még ha több kiadója is van.
    - game_publisher: appid + pubid (1-től generált)
    - publishers: pubid + name (összefűzött kiadók)
    """
    rows = []

    for _, row in master_df.iterrows():
        appid = row["appid"]
        pubs_raw = row.get("publishers", "")
        if not pubs_raw or pd.isna(pubs_raw):
            continue

        if isinstance(pubs_raw, list):
            pub_list = [str(p).strip() for p in pubs_raw if str(p).strip()]
        else:
            pub_list = [p.strip() for p in str(pubs_raw).split(",") if p.strip()]

        if not pub_list:
            continue

        combined_pubs = ", ".join(pub_list)
        rows.append({"appid": appid, "publisher_name": combined_pubs})

    df_flat = pd.DataFrame(rows).reset_index(drop=True)

    df_flat.insert(1, "pubid", range(1, len(df_flat)+1))

    game_publisher_df = df_flat[['appid', 'pubid']].copy()
    publishers_df = df_flat[['pubid', 'publisher_name']].copy()

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        publishers_path = os.path.join(output_dir, "publishers.csv")
        game_publisher_path = os.path.join(output_dir, "game_publisher.csv")
        publishers_df.to_csv(publishers_path, index=False)
        game_publisher_df.to_csv(game_publisher_path, index=False)
        logging.info(f"Saved 'publishers.csv' ({len(publishers_df)} rows) to {output_dir}")
        logging.info(f"Saved 'game_publisher.csv' ({len(game_publisher_df)} rows) to {output_dir}")

    return publishers_df, game_publisher_df

