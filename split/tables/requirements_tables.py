#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import ast
import pandas as pd
import logging
from utils.text_utils import clean_requirements_text, split_min_rec

def create_requirements_table(master_df: pd.DataFrame, output_dir: str = None) -> pd.DataFrame:
    rows = []

    for _, r in master_df.iterrows():
        appid = r['appid']

        # --- Windows (pc_requirements) ---
        pc_val = r.get('pc_requirements', "")
        if pd.notna(pc_val) and str(pc_val).strip():
            try:
                val_dict = ast.literal_eval(pc_val)
                win_min = clean_requirements_text(val_dict.get('minimum', ""))
                win_rec = clean_requirements_text(val_dict.get('recommended', ""))
            except Exception:
                text = clean_requirements_text(pc_val)
                win_min, win_rec = split_min_rec(text)

            if win_min:
                win_min, extra_rec = split_min_rec(win_min)
                if win_min:
                    rows.append({'appid': appid, 'os': 'windows', 'type': 'minimum', 'requirements': win_min})
                if extra_rec:
                    rows.append({'appid': appid, 'os': 'windows', 'type': 'recommended', 'requirements': extra_rec})

            if win_rec:
                rows.append({'appid': appid, 'os': 'windows', 'type': 'recommended', 'requirements': win_rec})


        # --- Mac ---
        val = r.get('mac_requirements', "")
        if pd.notna(val):
            val_str = str(val).strip()
            if val_str and val_str not in ["[]", "{}", "nan", "None"]:
                try:
                    val_dict = ast.literal_eval(val)
                    min_val = val_dict.get('minimum', "")
                    rec_val = val_dict.get('recommended', "")
                except Exception:
                    min_val = val
                    rec_val = ""

                min_val = clean_requirements_text(min_val)
                rec_val = clean_requirements_text(rec_val)

                if min_val:
                    min_val, extra_rec = split_min_rec(min_val)
                    if min_val:
                        rows.append({'appid': appid, 'os': 'mac', 'type': 'minimum', 'requirements': min_val})
                    if extra_rec:
                        rows.append({'appid': appid, 'os': 'mac', 'type': 'recommended', 'requirements': extra_rec})
                if rec_val:
                    rows.append({'appid': appid, 'os': 'mac', 'type': 'recommended', 'requirements': rec_val})

        # --- Linux ---
        val = r.get('linux_requirements', "")
        if pd.notna(val):
            val_str = str(val).strip()
            if val_str and val_str not in ["[]", "{}", "nan", "None"]:
                try:
                    val_dict = ast.literal_eval(val)
                    min_val = val_dict.get('minimum', "")
                    rec_val = val_dict.get('recommended', "")
                except Exception:
                    min_val = val
                    rec_val = ""

                min_val = clean_requirements_text(min_val)
                rec_val = clean_requirements_text(rec_val)

                if min_val:
                    min_val, extra_rec = split_min_rec(min_val)
                    if min_val:
                        rows.append({'appid': appid, 'os': 'linux', 'type': 'minimum', 'requirements': min_val})
                    if extra_rec:
                        rows.append({'appid': appid, 'os': 'linux', 'type': 'recommended', 'requirements': extra_rec})
                if rec_val:
                    rows.append({'appid': appid, 'os': 'linux', 'type': 'recommended', 'requirements': rec_val})



    df_req = pd.DataFrame(rows)
    if not df_req.empty:
        df_req.insert(0, 'reqid', range(1, len(df_req)+1))

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "requirements.csv")
        df_req.to_csv(path, index=False)
        logging.info(f"Saved 'requirements.csv' ({len(df_req)} rows) to {output_dir}")

    return df_req

