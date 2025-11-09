#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd
import logging
from typing import Any

# ======== HELPER FUNCTIONS ========
def load_csv_safely(path: str, **kwargs: Any) -> pd.DataFrame:
    """
    Betölt egy CSV fájlt, hiba esetén üres DataFrame-et ad vissza.
    """
    try:
        df = pd.read_csv(path, **kwargs)
        logging.info(f"Loaded: {os.path.basename(path)} ({len(df)} rows)")
        return df
    except Exception as e:
        logging.error(f"Error loading {path}: {e}")
        return pd.DataFrame()

