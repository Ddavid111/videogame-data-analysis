import os
import ast

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


# =========================================
# CONFIG
# =========================================
BASE_PATH = r"C:\Users\zalma\videogame-data-analysis"
MERGED_PATH = os.path.join(BASE_PATH, "merge", "merged_master.csv")
OUTPUT_DIR = os.path.join(BASE_PATH, "merge", "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================================
# HELPERS
# =========================================
def parse_genres(val):
    if pd.isna(val):
        return []

    if isinstance(val, list):
        return [v.strip() for v in val if isinstance(v, str) and v.strip()]

    if isinstance(val, str):
        try:
            parsed = ast.literal_eval(val)
            if isinstance(parsed, list):
                return [str(v).strip() for v in parsed if str(v).strip()]
        except Exception:
            pass

        if "," in val:
            return [v.strip() for v in val.split(",") if v.strip()]

        return [val.strip()]

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
# STEP 1 – Összes játék évente
# =========================================
def plot_all_years(df, latest_year, latest_month, month_names, output_dir):
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


# =========================================
# STEP 1/B – 2010 előtti játékok
# =========================================
def plot_pre2010(df, latest_year, latest_month, month_names, output_dir):
    df_pre2010 = df[df["year"] < 2010]
    if df_pre2010.empty:
        return

    years = sorted(df_pre2010["year"].unique())
    counts = df_pre2010["year"].value_counts().sort_index()

    plt.figure(figsize=(14, 6))
    plt.bar(range(len(years)), counts.values, color="steelblue")

    plt.title("Játékok száma évente – 2010 előtt")
    plt.xlabel("Év")
    plt.ylabel("Játékok száma")
    plt.tight_layout()

    ax = plt.gca()
    apply_latest_year_label(ax, years, latest_year, latest_month, month_names)

    out_path = os.path.join(output_dir, "hist_pre2010.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.show()
    print(f"Mentve: {out_path}")


# =========================================
# STEP 1/C – 2010 utáni játékok
# =========================================
def plot_post2010(df, latest_year, latest_month, month_names, output_dir):
    df_post2010 = df[df["year"] >= 2010]
    if df_post2010.empty:
        return

    years = sorted(df_post2010["year"].unique())
    counts = df_post2010["year"].value_counts().sort_index()

    plt.figure(figsize=(14, 6))
    plt.bar(range(len(years)), counts.values, color="steelblue")

    plt.title("Játékok száma évente – 2010 után")
    plt.xlabel("Év")
    plt.ylabel("Játékok száma")

    ax = plt.gca()
    apply_latest_year_label(ax, years, latest_year, latest_month, month_names)

    out_path = os.path.join(output_dir, "hist_post2010.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.show()
    print(f"Mentve: {out_path}")


# =========================================
# STEP 2 – Forrás szerinti bontás (C, B, A)
# =========================================
def plot_by_sources(df, latest_year, latest_month, month_names, output_dir):
    if "sources" not in df.columns:
        return

    sources_order = ["C", "B", "A"]

    for src in sources_order:
        df_source = df[df["sources"] == src]
        if df_source.empty:
            continue

        years = sorted(df_source["year"].unique())
        counts = df_source["year"].value_counts().sort_index()

        plt.figure(figsize=(14, 6))
        plt.plot(range(len(years)), counts.values, marker="o", linewidth=2)

        plt.title(f"Játékok száma évente – {src}")
        ax = plt.gca()
        apply_latest_year_label(ax, years, latest_year, latest_month, month_names)

        out_path = os.path.join(output_dir, f"hist_sources_{src}.png")
        plt.savefig(out_path, dpi=300, bbox_inches="tight")
        plt.show()
        print(f"Mentve: {out_path}")


# =========================================
# STEP 3 – Top 5 genre overlay
# =========================================
def plot_genres(df, latest_year, latest_month, month_names, output_dir):
    if "genres" not in df.columns:
        return

    df["genres_list"] = df["genres"].apply(parse_genres)
    df_exp = df.explode("genres_list").dropna(subset=["genres_list"])

    top_genres = df_exp["genres_list"].value_counts().nlargest(5).index
    df_top = df_exp[df_exp["genres_list"].isin(top_genres)]

    pivot = df_top.groupby(["year", "genres_list"]).size().unstack(fill_value=0)
    years = sorted(pivot.index)

    plt.figure(figsize=(14, 7))

    for genre in top_genres:
        vals = pivot[genre].reindex(years, fill_value=0)
        plt.plot(range(len(years)), vals.values, marker="o", linewidth=2, label=genre)

    ax = plt.gca()
    apply_latest_year_label(ax, years, latest_year, latest_month, month_names)

    plt.legend(title="Top 5 műfaj")
    plt.tight_layout()

    out_path = os.path.join(output_dir, "hist_genres_top5.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.show()
    print(f"Mentve: {out_path}")


# =========================================
# STEP 4 – Éves növekedési ráta (fold-change)
# =========================================
def plot_growth_rates(df, output_dir):
    """
    Éves hányszoros növekedés (fold-change) vizualizációja logaritmikus skálán.
    """
    counts = df["year"].value_counts().sort_index()
    growth = counts / counts.shift(1)

    years = counts.index.tolist()
    growth_vals = growth.values

    plt.figure(figsize=(14, 6))
    plt.plot(years, growth_vals, marker="o", linewidth=2)

    plt.axhline(1.0, color="gray", linestyle="--", linewidth=1)

    plt.title("Éves növekedési ráta (hányszorosára változott)")
    plt.xlabel("Év")
    plt.ylabel("Növekedési faktor (x)")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)

    out_path = os.path.join(output_dir, "hist_growth_rates.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.show()
    print(f"Mentve: {out_path}")


# =========================================
# STEP 5 – Szezonális overlay-ek (havi / heti / napi)
# =========================================
def plot_monthly_overlay(df, output_dir):
    df = df.copy()
    df["date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df = df.dropna(subset=["date"])

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    monthly = df.groupby(["year", "month"]).size().unstack(fill_value=0)

    plt.figure(figsize=(14, 7))

    for year in monthly.index:
        plt.plot(range(1, 13), monthly.loc[year], marker="o", linewidth=2, label=year)

    plt.xticks(range(1, 13))
    plt.xlabel("Hónap")
    plt.ylabel("Játékmegjelenések száma")
    plt.title("Játékmegjelenések havi bontásban – évek egymásra rajzolva")
    plt.grid(True, alpha=0.3)
    plt.legend(ncol=2, fontsize=8)

    out_path = os.path.join(output_dir, "seasonal_monthly_overlay.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.show()
    print(f"Mentve: {out_path}")


def plot_weekly_overlay(df, output_dir):
    df = df.copy()
    df["date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df = df.dropna(subset=["date"])

    df["year"] = df["date"].dt.year
    df["week"] = df["date"].dt.isocalendar().week.astype(int)

    weekly = df.groupby(["year", "week"]).size().unstack(fill_value=0)

    plt.figure(figsize=(16, 7))

    for year in weekly.index:
        plt.plot(range(1, 54), weekly.loc[year], linewidth=1, alpha=0.8, label=year)

    plt.xlabel("Hét")
    plt.ylabel("Játékmegjelenések száma")
    plt.title("Játékmegjelenések heti bontásban – évek egymásra rajzolva")
    plt.grid(True, alpha=0.3)
    plt.legend(ncol=3, fontsize=7)

    out_path = os.path.join(output_dir, "seasonal_weekly_overlay.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.show()
    print(f"Mentve: {out_path}")


def plot_daily_overlay(df, output_dir):
    df = df.copy()
    df["date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df = df.dropna(subset=["date"])

    df["year"] = df["date"].dt.year
    df["dayofyear"] = df["date"].dt.dayofyear

    daily = df.groupby(["year", "dayofyear"]).size().unstack(fill_value=0)

    plt.figure(figsize=(16, 7))

    for year in daily.index:
        plt.plot(range(1, 367), daily.loc[year], linewidth=1, alpha=0.5, label=year)

    plt.xlabel("Nap (1–365)")
    plt.ylabel("Játékmegjelenések száma")
    plt.title("Játékmegjelenések napi bontásban – évek egymásra rajzolva")
    plt.grid(True, alpha=0.3)
    plt.legend(ncol=4, fontsize=7)

    out_path = os.path.join(output_dir, "seasonal_daily_overlay.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.show()
    print(f"Mentve: {out_path}")


# =========================================
# STEP 6 – Hőtérkép: év × nap
# =========================================
def plot_heatmap_year_day(df, output_dir):
    """
    Hőtérkép: sorok = évek, oszlopok = napok (1–365)
    Érték: adott év adott napján megjelent játékok száma.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df = df.dropna(subset=["date"])

    df["year"] = df["date"].dt.year
    df["dayofyear"] = df["date"].dt.dayofyear

    heat = df.groupby(["year", "dayofyear"]).size().unstack(fill_value=0)
    heat = heat.reindex(columns=range(1, 366), fill_value=0)

    plt.figure(figsize=(22, 10))
    plt.imshow(heat, aspect="auto", cmap="hot", interpolation="nearest")

    plt.colorbar(label="Megjelenések száma")
    plt.title("Játékmegjelenések hőtérképe – év × nap", fontsize=18)
    plt.xlabel("Nap (1–365)")
    plt.ylabel("Év")

    plt.yticks(ticks=np.arange(len(heat.index)), labels=heat.index)

    out_path = os.path.join(output_dir, "heatmap_year_day.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.show()
    print(f"Mentve: {out_path}")


# =========================================
# STEP 7 – 2026 előrejelzés (logaritmikus trend, modern éra)
# =========================================
def forecast_2026(df, output_dir):
    """
    2026-os játékmegjelenés-szám becslése logaritmikus trenddel,
    csak a modern évekre (2014–2024) illesztve.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["year"] = df["date"].dt.year

    counts = df["year"].value_counts().sort_index()

    modern = counts[(counts.index >= 2014) & (counts.index <= 2024)]

    years = np.array(modern.index).reshape(-1, 1)
    values = modern.values
    log_values = np.log(values)

    model = LinearRegression()
    model.fit(years, log_values)

    log_pred = model.predict(np.array([[2026]]))
    pred_2026 = float(np.exp(log_pred)[0])

    print("\n=== 2026 logaritmikus előrejelzés (modern évek alapján) ===")
    print(f"Előrejelzés: ~{pred_2026:.0f} játék")
    print("============================================================\n")

    plt.figure(figsize=(12, 6))
    plt.scatter(modern.index, modern.values, label="Modern adatok (2014–2024)")

    x_range = np.arange(2014, 2027)
    y_curve = np.exp(model.predict(x_range.reshape(-1, 1)))
    plt.plot(x_range, y_curve, color="orange", label="Logaritmikus trend (2014–2024)")

    plt.scatter([2026], [pred_2026], color="red",
                label=f"2026 becslés: {pred_2026:.0f}")

    plt.title("Játékmegjelenések – logaritmikus trend (modern érából)")
    plt.xlabel("Év")
    plt.ylabel("Megjelenések száma")
    plt.legend()

    out_path = os.path.join(output_dir, "forecast_2026_log_modern.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.show()
    print(f"Mentve: {out_path}")

    return pred_2026


# =========================================
# MAIN PLOTTING LOGIC (fővezérlés)
# =========================================
def plot_histograms(df: pd.DataFrame, output_dir: str):
    df["date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df = df.dropna(subset=["year"]).copy()
    df["year"] = df["year"].astype(int)

    latest_year = int(df["year"].max())
    latest_month = int(df[df["year"] == latest_year]["month"].max())

    month_names = {
        1: "január", 2: "február", 3: "március",
        4: "április", 5: "május", 6: "június",
        7: "július", 8: "augusztus", 9: "szeptember",
        10: "október", 11: "november", 12: "december",
    }

    plot_all_years(df, latest_year, latest_month, month_names, output_dir)
    plot_pre2010(df, latest_year, latest_month, month_names, output_dir)
    plot_post2010(df, latest_year, latest_month, month_names, output_dir)

    plot_by_sources(df, latest_year, latest_month, month_names, output_dir)

    plot_genres(df, latest_year, latest_month, month_names, output_dir)

    plot_growth_rates(df, output_dir)

    plot_monthly_overlay(df, output_dir)
    plot_weekly_overlay(df, output_dir)
    plot_daily_overlay(df, output_dir)

    plot_heatmap_year_day(df, output_dir)

    forecast_2026(df, output_dir)


# =========================================
# ENTRY POINT
# =========================================
def main():
    print("=== Hisztogramok generálása indul ===")
    df = pd.read_csv(MERGED_PATH, low_memory=False)
    plot_histograms(df, OUTPUT_DIR)
    print("=== Hisztogramok elkészültek és fájlba mentve. ===")
