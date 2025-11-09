#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import ast
import pandas as pd
import logging

def create_tags_table(master_df: pd.DataFrame, output_dir: str = None):
    """
    Egyszerűsített tags táblageneráló függvény.
    A merged_master.csv 'tags' oszlopából két táblát készít:
      - game_tag.csv: appid–tagid kapcsolatok
      - tags.csv: tagid–tag_name–weight lista
    """
    rows_game_tag = []
    rows_tags = []
    tagid_counter = 1

    for _, row in master_df.iterrows():
        appid = row["appid"]
        tags_val = row.get("tags")

        if not tags_val or pd.isna(tags_val):
            continue

        if isinstance(tags_val, str):
            try:
                tags_val = ast.literal_eval(tags_val)
            except Exception:
                continue

        if not isinstance(tags_val, list):
            continue

        for tag_entry in tags_val:
            if not isinstance(tag_entry, dict):
                continue
            tag_name = tag_entry.get("tag_name")
            weight = tag_entry.get("weight", 1)

            if not tag_name:
                continue

            rows_game_tag.append({"appid": appid, "tagid": tagid_counter})
            rows_tags.append({"tagid": tagid_counter, "tag_name": tag_name, "weight": weight})
            tagid_counter += 1

    game_tag_df = pd.DataFrame(rows_game_tag)
    tags_df = pd.DataFrame(rows_tags)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        game_tag_path = os.path.join(output_dir, "game_tag.csv")
        tags_path = os.path.join(output_dir, "tags.csv")

        game_tag_df.to_csv(game_tag_path, index=False, encoding="utf-8-sig")
        tags_df.to_csv(tags_path, index=False, encoding="utf-8-sig")

        logging.info(f"Saved 'game_tag.csv' ({len(game_tag_df)} rows) to {output_dir}")
        logging.info(f"Saved 'tags.csv' ({len(tags_df)} rows) to {output_dir}")

    return game_tag_df, tags_df

