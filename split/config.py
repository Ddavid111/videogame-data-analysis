"""
Globális konfigurációs beállítások a split folyamat számára.
"""

import os
import logging

# ======== ALAP MAPPÁK ========
BASE_PATH = r"C:\Users\zalma"

MERGE_PATH = os.path.join(BASE_PATH, "merge")
OUTPUT_PATH = os.path.join(BASE_PATH, "split")

# ======== BEMENETI FÁJL ========
MERGED_MASTER_FILE = os.path.join(MERGE_PATH, "merged_master.csv")

# ======== LOGGING ========
LOG_FILE = os.path.join(OUTPUT_PATH, "split_log.txt")

# ======== LOGGING KONFIG ========
os.makedirs(OUTPUT_PATH, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ],
)
