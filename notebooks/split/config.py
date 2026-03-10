"""
Global configuration settings for the split process.
"""

import os
import logging

# ======== BASE PATHS ========
NOTEBOOKS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(NOTEBOOKS_ROOT, ".."))

MERGE_PATH = os.path.join(NOTEBOOKS_ROOT, "merge")
OUTPUT_PATH = os.path.join(NOTEBOOKS_ROOT, "split")
GENERATED_PATH = os.path.join(OUTPUT_PATH, "generated")
TABLES_OUTPUT_PATH = os.path.join(GENERATED_PATH, "tables")
LOGS_OUTPUT_PATH = os.path.join(GENERATED_PATH, "logs")

MEDIA_TABLES_PATH = os.path.join(TABLES_OUTPUT_PATH, "media")
SUPPORT_TABLES_PATH = os.path.join(TABLES_OUTPUT_PATH, "support")
REQUIREMENTS_TABLES_PATH = os.path.join(TABLES_OUTPUT_PATH, "requirements")
PLATFORMS_TABLES_PATH = os.path.join(TABLES_OUTPUT_PATH, "platforms")
PACKAGES_TABLES_PATH = os.path.join(TABLES_OUTPUT_PATH, "packages")
PEOPLE_TABLES_PATH = os.path.join(TABLES_OUTPUT_PATH, "people")
GENRES_TABLES_PATH = os.path.join(TABLES_OUTPUT_PATH, "genres")
TAGS_TABLES_PATH = os.path.join(TABLES_OUTPUT_PATH, "tags")
METADATA_TABLES_PATH = os.path.join(TABLES_OUTPUT_PATH, "metadata")
LANGUAGE_TABLES_PATH = os.path.join(TABLES_OUTPUT_PATH, "languages")

# ======== INPUT FILE ========
MERGED_MASTER_FILE = os.path.join(
    MERGE_PATH, "generated", "tables", "merged_master.csv"
)
LEGACY_MERGED_MASTER_FILE = os.path.join(MERGE_PATH, "merged_master.csv")
if not os.path.exists(MERGED_MASTER_FILE) and os.path.exists(LEGACY_MERGED_MASTER_FILE):
    MERGED_MASTER_FILE = LEGACY_MERGED_MASTER_FILE

# ======== LOGGING ========
LOG_FILE = os.path.join(LOGS_OUTPUT_PATH, "split_log.txt")

# ======== LOGGING CONFIG ========
os.makedirs(OUTPUT_PATH, exist_ok=True)
os.makedirs(GENERATED_PATH, exist_ok=True)
os.makedirs(TABLES_OUTPUT_PATH, exist_ok=True)
os.makedirs(LOGS_OUTPUT_PATH, exist_ok=True)
os.makedirs(MEDIA_TABLES_PATH, exist_ok=True)
os.makedirs(SUPPORT_TABLES_PATH, exist_ok=True)
os.makedirs(REQUIREMENTS_TABLES_PATH, exist_ok=True)
os.makedirs(PLATFORMS_TABLES_PATH, exist_ok=True)
os.makedirs(PACKAGES_TABLES_PATH, exist_ok=True)
os.makedirs(PEOPLE_TABLES_PATH, exist_ok=True)
os.makedirs(GENRES_TABLES_PATH, exist_ok=True)
os.makedirs(TAGS_TABLES_PATH, exist_ok=True)
os.makedirs(METADATA_TABLES_PATH, exist_ok=True)
os.makedirs(LANGUAGE_TABLES_PATH, exist_ok=True)

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
