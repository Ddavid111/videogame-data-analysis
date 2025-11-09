#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# ======== IMPORTOK ========
import os
import pandas as pd
import logging

from merge.utils.io_utils import load_csv_safely
from merge.utils.clean_utils import clean_columns


# ======== SOURCE C LOADING ========
def load_source_c(c_path: str) -> pd.DataFrame:
    """
    Betölti a C forrást több CSV fájlból, megtisztítja az oszlopneveket,
    és egyesíti az adatokat egy DataFrame-be.
    """
    c_files = [
        "games_march2025_cleaned.csv",
        "games_march2025_full.csv",
        "games_may2024_cleaned.csv",
        "games_may2024_full.csv",
    ]
    c_dfs = [load_csv_safely(os.path.join(c_path, f)) for f in c_files]
    c_dfs = [clean_columns(df) for df in c_dfs if not df.empty]
    df_c = pd.concat(c_dfs, ignore_index=True)
    df_c["appid"] = df_c["appid"].astype(str)
    logging.info(f"C source combined: {len(df_c)} rows")
    return df_c

