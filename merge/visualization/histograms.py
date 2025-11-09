#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import ast
import os


# =========================================
# CONFIG
# =========================================
BASE_PATH = r"C:\Users\zalma"
MERGED_PATH = os.path.join(BASE_PATH, "merge", "merged_master.csv")
OUTPUT_DIR = os.path.join(BASE_PATH, "merge", "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================================
# HELPER FUNCTIONS
# =========================================
def parse_genres(val):
    """
    A genres oszlopot listává alakítja.
    Kezeli a stringként tárolt listákat és a sima szöveget is.
    """
    if pd.isna(val):
        return []
    try:
        parsed = ast.literal_eval(val) if isinstance(val, str) else val
        if isinstance(parsed, list):
            return [str(v).strip() for v in parsed if v and str(v).strip()]
        if isinstance(parsed, str):
            return [v.strip() for v in parsed.split(",") if v.strip()]
    except Exception:
        pass
    return []


# =========================================
# MAIN PLOTTING LOGIC
# =========================================
def plot_histograms(df: pd.DataFrame, output_dir: str):
    """
    Három hisztogramot készít a merged_master.csv adatai alapján, és fájlba menti:
    1. Összes játék évente
    2. Forrásonként (sources)
    3. Top 5 műfaj szerint (genres)
    """

    df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
    df = df.dropna(subset=["year"]).copy()
    df["year"] = df["year"].astype(int)

    plt.figure(figsize=(10, 6))
    df["year"].value_counts().sort_index().plot(kind="bar", color="steelblue")
    plt.title("Játékok száma évente")
    plt.xlabel("Év")
    plt.ylabel("Játékok száma")
    plt.tight_layout()
    all_path = os.path.join(output_dir, "hist_all_years.png")
    plt.savefig(all_path, dpi=300)
    plt.show()
    print(f"Mentve: {all_path}")

    if "sources" in df.columns:
        plt.figure(figsize=(10, 6))
        df.groupby(["year", "sources"]).size().unstack(fill_value=0).plot(kind="bar", stacked=True)
        plt.title("Játékok száma évente – forrás szerint")
        plt.xlabel("Év")
        plt.ylabel("Játékok száma")
        plt.tight_layout()
        src_path = os.path.join(output_dir, "hist_sources.png")
        plt.savefig(src_path, dpi=300)
        plt.show()
        print(f"Mentve: {src_path}")

    if "genres" in df.columns:
        df["genres_list"] = df["genres"].apply(parse_genres)
        df_exploded = df.explode("genres_list").dropna(subset=["genres_list"])

        top_genres = df_exploded["genres_list"].value_counts().nlargest(5).index
        df_top = df_exploded[df_exploded["genres_list"].isin(top_genres)]

        plt.figure(figsize=(10, 6))
        df_top.groupby(["year", "genres_list"]).size().unstack(fill_value=0).plot(kind="bar", stacked=True)
        plt.title("Játékok száma évente – top 5 műfaj")
        plt.xlabel("Év")
        plt.ylabel("Játékok száma")
        plt.tight_layout()
        genre_path = os.path.join(output_dir, "hist_genres_top5.png")
        plt.savefig(genre_path, dpi=300)
        plt.show()
        print(f"Mentve: {genre_path}")


# =========================================
# ENTRY POINT
# =========================================
def main():
    print("=== Hisztogramok generálása indul ===")
    df = pd.read_csv(MERGED_PATH, low_memory=False)
    plot_histograms(df, OUTPUT_DIR)
    print("=== Hisztogramok elkészültek és fájlba mentve. ===")

