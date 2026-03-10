# ======== IMPORTOK ========
import os
import logging

# ======== PATHS ========
NOTEBOOKS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(NOTEBOOKS_ROOT, ".."))
DATA_PATH = os.path.join(PROJECT_ROOT, "data")
A_PATH = os.path.join(DATA_PATH, "A")
B_PATH = os.path.join(DATA_PATH, "B")
C_PATH = os.path.join(DATA_PATH, "C")
OUTPUT_PATH = os.path.join(NOTEBOOKS_ROOT, "merge")
GENERATED_PATH = os.path.join(OUTPUT_PATH, "generated")
SOURCES_OUTPUT_PATH = os.path.join(GENERATED_PATH, "sources")
TABLES_OUTPUT_PATH = os.path.join(GENERATED_PATH, "tables")
REPORTS_OUTPUT_PATH = os.path.join(GENERATED_PATH, "reports")
VENN_OUTPUT_PATH = os.path.join(GENERATED_PATH, "venn")
PLOTS_OUTPUT_PATH = os.path.join(GENERATED_PATH, "plots")
LOGS_OUTPUT_PATH = os.path.join(GENERATED_PATH, "logs")

# ======== LOGGING CONFIGURATION ========
os.makedirs(OUTPUT_PATH, exist_ok=True)
os.makedirs(GENERATED_PATH, exist_ok=True)
os.makedirs(SOURCES_OUTPUT_PATH, exist_ok=True)
os.makedirs(TABLES_OUTPUT_PATH, exist_ok=True)
os.makedirs(REPORTS_OUTPUT_PATH, exist_ok=True)
os.makedirs(VENN_OUTPUT_PATH, exist_ok=True)
os.makedirs(PLOTS_OUTPUT_PATH, exist_ok=True)
os.makedirs(LOGS_OUTPUT_PATH, exist_ok=True)
LOG_FILE = os.path.join(LOGS_OUTPUT_PATH, "merge_log.txt")

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
        logging.StreamHandler(),
    ],
    force=True,
)
