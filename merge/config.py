# ======== IMPORTOK ========
import os
import logging

# ======== PATHS ========
BASE_PATH = os.path.expanduser(r"C:\Users\zalma")
A_PATH = os.path.join(BASE_PATH, "A")
B_PATH = os.path.join(BASE_PATH, "B")
C_PATH = os.path.join(BASE_PATH, "C")
OUTPUT_PATH = os.path.join(BASE_PATH, r"videogame-data-analysis\merge")

# ======== LOGGING CONFIGURATION ========
os.makedirs(OUTPUT_PATH, exist_ok=True)
LOG_FILE = os.path.join(OUTPUT_PATH, "merge_log.txt")

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
