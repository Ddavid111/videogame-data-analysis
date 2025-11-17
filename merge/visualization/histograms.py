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
# HELPERS
# =========================================
def parse_genres(val):
    if pd.isna(val):
        return []
    try:
        parsed = ast.literal_eval(val) if isinstance(val, str) else val
        if isinstance(parsed, list):
            return [str(v).strip() for v in parsed if v and str(v).strip()]
        if isinstance(parsed, str):
            return [v.strip() for v in parsed.split(",") if v.strip()]
    except (ValueError, SyntaxError, TypeError):
        # If parsing fails, return empty list
        return []
    return []


def apply_latest_year_label(ax, years, latest_year, latest_month, month_names):
    tick_positions = list(range(len(years)))
    tick_labels = []

    for y in years:
        if y == latest_year:
            tick_labels.append(f"{y} ({month_names[latest_month]}ig)")
        else:
            tick_labels.append(str(y))

    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45, ha="right")


# =========================================
# MAIN PLOTTING LOGIC
# =========================================
def plot_histograms(df: pd.DataFrame, output_dir: str):

    # ----------------------------
    # Dátumok feldolgozása
    # ----------------------------
    df["date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df = df.dropna(subset=["year"]).copy()
    df["year"] = df["year"].astype(int)

    # ----------------------------
    # Legfrissebb év + hónap
    # ----------------------------
    latest_year = int(df["year"].max())
    latest_month = int(df[df["year"] == latest_year]["month"].max())

    month_names = {
        1: "január", 2: "február", 3: "március",
        4: "április", 5: "május", 6: "június",
        7: "július", 8: "augusztus", 9: "szeptember",
        10: "október", 11: "november", 12: "december"
    }

    # ==========================================================
    # 1) ÖSSZES JÁTÉK ÉVENTE
    # ==========================================================
    years = sorted(df["year"].unique())
    counts = df["year"].value_counts().sort_index()

    plt.figure(figsize=(14, 6))
    plt.bar(range(len(years)), counts.values, color="steelblue")

    plt.title("Játékok száma évente")
    plt.xlabel("Év")
    plt.ylabel("Játékok száma")
    plt.tight_layout()

    ax = plt.gca()
    apply_latest_year_label(ax, years, latest_year, latest_month, month_names)

    output_path = os.path.join(output_dir, "hist_all_years.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.show()
    print(f"Mentve: {output_path}")

    # ==========================================================
    # 1/B) 2010 ELŐTTI JÁTÉKOK
    # ==========================================================
    df_pre2010 = df[df["year"] < 2010]

    if not df_pre2010.empty:
        years_pre = sorted(df_pre2010["year"].unique())
        counts_pre = df_pre2010["year"].value_counts().sort_index()

        plt.figure(figsize=(14, 6))
        plt.bar(range(len(years_pre)), counts_pre.values, color="steelblue")

        plt.title("Játékok száma évente – 2010 előtt")
        plt.xlabel("Év")
        plt.ylabel("Játékok száma")
        plt.tight_layout()

        ax = plt.gca()
        apply_latest_year_label(
            ax, years_pre, latest_year, latest_month, month_names
        )

        out_pre = os.path.join(output_dir, "hist_pre2010.png")
        plt.savefig(out_pre, dpi=300, bbox_inches="tight")
        plt.show()
        print(f"Mentve: {out_pre}")

    # ==========================================================
    # 1/C) 2010 UTÁNI JÁTÉKOK
    # ==========================================================
    df_post2010 = df[df["year"] >= 2010]

    if not df_post2010.empty:
        years_post = sorted(df_post2010["year"].unique())
        counts_post = df_post2010["year"].value_counts().sort_index()

        plt.figure(figsize=(14, 6))
        plt.bar(range(len(years_post)), counts_post.values, color="steelblue")

        plt.title("Játékok száma évente – 2010 után")
        plt.xlabel("Év")
        plt.ylabel("Játékok száma")
        ax = plt.gca()
        apply_latest_year_label(
            ax, years_post, latest_year, latest_month, month_names
        )

        out_post = os.path.join(output_dir, "hist_post2010.png")

        out_post = os.path.join(output_dir, "hist_post2010.png")
        plt.savefig(out_post, dpi=300, bbox_inches="tight")
        plt.show()
        print(f"Mentve: {out_post}")

    # ==========================================================
    # 2) FORRÁS SZERINT – 3 KÜLÖN ÁBRA: C, B, A
    # ==========================================================
    if "sources" in df.columns:

        sources_order = ["C", "B", "A"]

        for src in sources_order:

            df_source = df[df["sources"] == src]
            if df_source.empty:
                continue

            years_src = sorted(df_source["year"].unique())
            counts_src = df_source["year"].value_counts().sort_index()

            plt.figure(figsize=(14, 6))
            plt.plot(range(len(years_src)), counts_src.values,
                     marker="o", linewidth=2)

            plt.title(f"Játékok száma évente – {src}")
            ax = plt.gca()
            apply_latest_year_label(
                ax, years_src, latest_year, latest_month, month_names
            )

            file_path = os.path.join(output_dir, f"hist_sources_{src}.png")
            ax = plt.gca()
            apply_latest_year_label(
                ax,
                years_src,
                latest_year,
                latest_month,
                month_names,
            )

            file_path = os.path.join(output_dir, f"hist_sources_{src}.png")
            plt.savefig(file_path, dpi=300, bbox_inches="tight")
            plt.show()
            print(f"Mentve: {file_path}")

    # ==========================================================
    # 3) TOP 5 GENRE – OVERLAY LINE CHART
    # ==========================================================
    if "genres" in df.columns:

        df["genres_list"] = df["genres"].apply(parse_genres)
        df_exp = df.explode("genres_list").dropna(subset=["genres_list"])

        top_genres = df_exp["genres_list"].value_counts().nlargest(5).index
        df_top = df_exp[df_exp["genres_list"].isin(top_genres)]

        pivot = df_top.groupby(["year", "genres_list"]) \
                      .size() \
                      .unstack(fill_value=0)

        years_genre = sorted(pivot.index)

        plt.figure(figsize=(14, 7))

        for genre in top_genres:
            y_vals = pivot[genre].reindex(years_genre, fill_value=0)
            plt.plot(range(len(years_genre)),
                     y_vals.values,
                     marker="o",
                     linewidth=2,
                     label=genre)

        ax = plt.gca()
        apply_latest_year_label(
            ax, years_genre, latest_year, latest_month, month_names
        )

        out_path = os.path.join(output_dir, "hist_genres_top5.png")
        plt.tight_layout()

        ax = plt.gca()
        apply_latest_year_label(
            ax,
            years_genre,
            latest_year,
            latest_month,
            month_names,
        )

        out_path = os.path.join(output_dir, "hist_genres_top5.png")
        plt.savefig(out_path, dpi=300, bbox_inches="tight")
        plt.show()
        print(f"Mentve: {out_path}")


# =========================================
# ENTRY POINT
# =========================================
def main():
    print("=== Hisztogramok generálása indul ===")
    df = pd.read_csv(MERGED_PATH, low_memory=False)
    plot_histograms(df, OUTPUT_DIR)
    print("=== Hisztogramok elkészültek és fájlba mentve. ===")
