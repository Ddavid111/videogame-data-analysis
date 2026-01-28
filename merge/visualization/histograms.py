import os
import ast

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
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
# STEP 3/B – Top 5 műfaj korreláció
# =========================================
def analyze_genre_correlation(df, start_year=2014, end_year=2024):
    if "genres" not in df.columns:
        return

    df = df.copy()
    df["genres_list"] = df["genres"].apply(parse_genres)
    df_exp = df.explode("genres_list").dropna(subset=["genres_list"])

    top_genres = df_exp["genres_list"].value_counts().nlargest(5).index
    df_top = df_exp[df_exp["genres_list"].isin(top_genres)]

    pivot = (
        df_top
        .groupby(["year", "genres_list"])
        .size()
        .unstack(fill_value=0)
        .loc[start_year:end_year]
    )

    print("\n=== Top 5 műfaj korreláció (Pearson) ===")
    corr = pivot.corr(method="pearson")
    print(corr.round(3))

    print("\n=== Top 5 műfaj korreláció (Spearman) ===")
    corr_s = pivot.corr(method="spearman")
    print(corr_s.round(3))

    return pivot, corr

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


def plot_weekly_overlay_from_daily(df, output_dir):
    df = df.copy()
    df["date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df = df.dropna(subset=["date"])

    df["year"] = df["date"].dt.year.astype(int)
    df["iso_week"] = df["date"].dt.isocalendar().week.astype(int)

    weekly = df.groupby(["year", "iso_week"]).size().unstack(fill_value=0)
    weekly = weekly.reindex(columns=range(1, 54), fill_value=0)

    plt.figure(figsize=(16, 7))
    for y in weekly.index:
        plt.plot(range(1, 54), weekly.loc[y].values, linewidth=1, alpha=0.6, label=y)

    plt.xlabel("ISO hét (1–53)")
    plt.ylabel("Megjelenések száma (heti)")
    plt.title("Heti bontás – évek egymásra rajzolva (weekday-hatás csökkentve)")
    plt.grid(True, alpha=0.3)
    plt.legend(ncol=4, fontsize=7)

    out_path = os.path.join(output_dir, "seasonal_weekly_overlay_iso.png")
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
    plt.imshow(heat, aspect="auto", cmap="viridis", norm=LogNorm(vmin=1, vmax=heat.values.max()))

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
# STEP 6/B – Hőtérkép: év × (ISO hét * 7 + hét napja)
# =========================================
def plot_heatmap_year_weekday_aligned(df, output_dir):
    """
    Hőtérkép, ahol a vízszintes tengely 52/53 hét * 7 nap.
    Így a hét napjai évek között egymásra igazodnak (erős weekday-minta jobban kijön).
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df = df.dropna(subset=["date"])

    iso = df["date"].dt.isocalendar()
    df["year"] = df["date"].dt.year.astype(int)
    df["iso_week"] = iso.week.astype(int)
    df["iso_weekday"] = iso.day.astype(int)

    df["week_day_idx"] = (df["iso_week"] - 1) * 7 + (df["iso_weekday"] - 1)

    heat = df.groupby(["year", "week_day_idx"]).size().unstack(fill_value=0)

    heat = heat.reindex(columns=range(0, 53 * 7), fill_value=0)

    plt.figure(figsize=(22, 10))
    plt.imshow(heat, aspect="auto", cmap="viridis", norm=LogNorm(vmin=1, vmax=heat.values.max()))

    plt.colorbar(label="Megjelenések száma")
    plt.title("Játékmegjelenések hőtérképe – év × (ISO hét × hét napja)", fontsize=18)
    plt.xlabel("Idő (hetek 1–53, naponként bontva)")
    plt.ylabel("Év")
    plt.yticks(ticks=np.arange(len(heat.index)), labels=heat.index)

    for x in range(0, 53 * 7, 7):
        plt.axvline(x - 0.5, linewidth=0.3, alpha=0.3)

    out_path = os.path.join(output_dir, "heatmap_year_weekday_aligned.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.show()
    print(f"Mentve: {out_path}")


# =========================================
# STEP 7 – Backtest + 2026 előrejelzés (logaritmikus trend, modern éra)
# =========================================
def forecast_year_log_modern(
    df,
    target_year: int,
    output_dir: str,
    train_start: int = 2014,
    train_end: int = 2024,
    show_plot: bool = True,
):
    """
    Log-trendes becslés modern évekre illesztve.

    Backtest-kompatibilis: a modell mindig csak a target_year-nál korábbi évekre tanul,
    így nem "látja" előre a cél-évet.

    Példa:
      - target_year=2024 -> tréning 2014–2023
      - target_year=2026 -> tréning 2014–2024 (ha train_end=2024)
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["year"] = df["date"].dt.year.astype(int)

    counts = df["year"].value_counts().sort_index()

    effective_train_end = min(train_end, target_year - 1)
    modern = counts[(counts.index >= train_start) & (counts.index <= effective_train_end)]

    if len(modern) < 3:
        raise ValueError(
            f"Túl kevés tréning év: {len(modern)} db (train: {train_start}–{effective_train_end})."
        )

    years = np.array(modern.index).reshape(-1, 1)
    values = modern.values.astype(float)

    if np.any(values <= 0):
        log_values = np.log(values + 1.0)
        add_one = True
    else:
        log_values = np.log(values)
        add_one = False

    model = LinearRegression()
    model.fit(years, log_values)

    log_pred = model.predict(np.array([[target_year]]))[0]
    pred = float(np.exp(log_pred) - (1.0 if add_one else 0.0))

    actual = float(counts.get(target_year, np.nan))

    print(f"\n=== Log előrejelzés (modern évek) → cél év: {target_year} ===")
    print(f"Tréning: {train_start}–{effective_train_end} (n={len(modern)})")
    print(f"Előrejelzés: ~{pred:.0f} játék")
    if not np.isnan(actual):
        err = pred - actual
        ape = abs(err) / actual * 100 if actual != 0 else np.nan
        print(f"Tényadat:    {actual:.0f} játék")
        print(f"Hiba:        {err:+.0f} játék | APE: {ape:.1f}%")
    else:
        print("Tényadat:    nincs az adathalmazban ehhez az évhez.")
    print("====================================================\n")

    if show_plot:
        plt.figure(figsize=(12, 6))
        plt.scatter(modern.index, modern.values, label=f"Tréning adatok ({train_start}–{effective_train_end})")

        x_min = train_start
        x_max = max(effective_train_end, target_year)
        x_range = np.arange(x_min, x_max + 1)

        y_curve = np.exp(model.predict(x_range.reshape(-1, 1)))
        if add_one:
            y_curve = y_curve - 1.0

        plt.plot(x_range, y_curve, color="orange", label="Log trend illesztés")

        plt.scatter([target_year], [pred], color="red", label=f"Becslés: {pred:.0f}")
        if not np.isnan(actual):
            plt.scatter([target_year], [actual], color="green", label=f"Tény: {actual:.0f}")

        plt.title("Játékmegjelenések – logaritmikus trend (modern éra)")
        plt.xlabel("Év")
        plt.ylabel("Megjelenések száma")
        plt.legend()

        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, f"forecast_{target_year}_log_modern.png")
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.show()
        print(f"Mentve: {out_path}")

    return pred, actual


def rolling_backtest_log_modern(
    df,
    test_years,
    output_dir,
    train_start: int = 2014,
    train_end: int = 2024,
    show_plots: bool = False,
):
    """
    Több évre lefuttatott backtest (rolling).
    """
    rows = []
    for y in test_years:
        pred, actual = forecast_year_log_modern(
            df,
            target_year=y,
            output_dir=output_dir,
            train_start=train_start,
            train_end=train_end,
            show_plot=show_plots,
        )

        if not np.isnan(actual) and actual != 0:
            ape = abs(pred - actual) / actual * 100
        else:
            ape = np.nan

        rows.append({"year": y, "pred": pred, "actual": actual, "APE_%": ape})

    res = pd.DataFrame(rows).sort_values("year")

    print("\n=== Rolling backtest összefoglaló ===")
    print(res.to_string(index=False, formatters={
        "pred": lambda v: f"{v:.0f}" if pd.notna(v) else "nan",
        "actual": lambda v: f"{v:.0f}" if pd.notna(v) else "nan",
        "APE_%": lambda v: f"{v:.1f}%" if pd.notna(v) else "nan"
    }))

    valid = res.dropna(subset=["APE_%"])
    if len(valid):
        print(f"\nÁtlagos APE: {valid['APE_%'].mean():.1f}% | Medián APE: {valid['APE_%'].median():.1f}%")

    return res


def forecast_2026(df, output_dir):
    """
    2026-os játékmegjelenés-szám becslése logaritmikus trenddel,
    modern évekre (2014–2024) illesztve.
    """
    pred_2026, _ = forecast_year_log_modern(df, target_year=2026, output_dir=output_dir, show_plot=True)
    print("\n=== 2026 logaritmikus előrejelzés (modern évek alapján) ===")
    print(f"Előrejelzés: ~{pred_2026:.0f} játék")
    print("============================================================\n")
    return pred_2026

def expanding_window_one_step_backtest_log_modern(
    df,
    output_dir: str,
    train_start: int = 2014,
    first_train_end: int = 2016,
    last_test_year: int = 2024,
    show_plot: bool = True,
):
    """
    Expanding-window 1-step backtest:
      tréning: train_start..t
      teszt:   t+1
    és nézi, hogyan változik a hiba, ahogy t nő (több tréningpont).
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["year"] = df["date"].dt.year.astype(int)
    counts = df["year"].value_counts().sort_index()

    rows = []

    for t in range(first_train_end, last_test_year):
        target_year = t + 1
        pred, actual = forecast_year_log_modern(
            df,
            target_year=target_year,
            output_dir=output_dir,
            train_start=train_start,
            train_end=t,
            show_plot=False,
        )

        if pd.notna(actual) and actual != 0:
            ape = abs(pred - actual) / actual * 100
        else:
            ape = np.nan

        rows.append({
            "train_end": t,
            "train_n": (t - train_start + 1),
            "target_year": target_year,
            "pred": pred,
            "actual": actual,
            "APE_%": ape,
        })

    res = pd.DataFrame(rows)

    print("\n=== Expanding-window 1-step backtest (log-modern) ===")
    print(res.to_string(index=False, formatters={
        "pred": lambda v: f"{v:.0f}" if pd.notna(v) else "nan",
        "actual": lambda v: f"{v:.0f}" if pd.notna(v) else "nan",
        "APE_%": lambda v: f"{v:.1f}%" if pd.notna(v) else "nan"
    }))

    valid = res.dropna(subset=["APE_%"])
    if len(valid):
        print(f"\nÁtlagos APE: {valid['APE_%'].mean():.1f}% | Medián APE: {valid['APE_%'].median():.1f}%")

    if show_plot:

        plt.figure(figsize=(12, 5))
        plt.plot(res["train_n"], res["APE_%"], marker="o")
        plt.title("Expanding-window backtest – hiba alakulása a tréningméret függvényében")
        plt.xlabel("Tréningévek száma (n)")
        plt.ylabel("APE (%)")
        plt.grid(True, alpha=0.3)

        out_path = os.path.join(output_dir, "expanding_backtest_ape_log_modern.png")
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.show()
        print(f"Mentve: {out_path}")

        res["error"] = res["pred"] - res["actual"]

        plt.figure(figsize=(12, 5))
        plt.plot(res["target_year"], res["error"], marker="o")
        plt.axhline(0, linewidth=1, linestyle="--")  # 0-vonal
        plt.title("Expanding-window backtest – előrejelzési hiba (becsült − valós)")
        plt.xlabel("Cél év")
        plt.ylabel("Hiba (játékok száma)")
        plt.grid(True, alpha=0.3)

        out_path2 = os.path.join(output_dir, "expanding_backtest_error_log_modern.png")
        plt.tight_layout()
        plt.savefig(out_path2, dpi=300)
        plt.show()
        print(f"Mentve: {out_path2}")

        plt.figure(figsize=(12, 5))
        plt.plot(res["target_year"], res["pred"], marker="o", label="Becsült")
        plt.plot(res["target_year"], res["actual"], marker="o", label="Valós")
        plt.title("Expanding-window backtest – becsült vs valós értékek")
        plt.xlabel("Cél év")
        plt.ylabel("Megjelenések száma")
        plt.grid(True, alpha=0.3)
        plt.legend()

        out_path3 = os.path.join(output_dir, "expanding_backtest_pred_vs_actual_log_modern.png")
        plt.tight_layout()
        plt.savefig(out_path3, dpi=300)
        plt.show()
        print(f"Mentve: {out_path3}")
        
    return res


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

    pivot, corr = analyze_genre_correlation(df)

    plot_growth_rates(df, output_dir)

    plot_monthly_overlay(df, output_dir)
    plot_weekly_overlay(df, output_dir)
    plot_weekly_overlay_from_daily(df, output_dir)

    plot_heatmap_year_day(df, output_dir)
    plot_heatmap_year_weekday_aligned(df, output_dir)

    expanding_window_one_step_backtest_log_modern(
        df,
        output_dir=output_dir,
        train_start=2014,
        first_train_end=2016,
        last_test_year=2024,
        show_plot=True,
    )
    
    forecast_year_log_modern(df, target_year=2024, output_dir=output_dir, show_plot=True)
    
    forecast_2026(df, output_dir)


# =========================================
# ENTRY POINT
# =========================================
def main():
    print("=== Hisztogramok generálása indul ===")
    df = pd.read_csv(MERGED_PATH, low_memory=False)
    plot_histograms(df, OUTPUT_DIR)
    print("=== Hisztogramok elkészültek és fájlba mentve. ===")
