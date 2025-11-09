#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# ======== IMPORTOK ========
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import logging


# ======== VENN DIAGRAM FUNCTIONS ========
def compute_venn_sets(a: pd.DataFrame, b: pd.DataFrame, c: pd.DataFrame):
    """Kiszámítja a halmazokat az appid alapján."""
    set_a = set(a["appid"].astype(str))
    set_b = set(b["appid"].astype(str))
    set_c = set(c["appid"].astype(str))

    only_a = set_a - set_b - set_c
    only_b = set_b - set_a - set_c
    only_c = set_c - set_a - set_b

    a_and_b = (set_a & set_b) - set_c
    a_and_c = (set_a & set_c) - set_b
    b_and_c = (set_b & set_c) - set_a

    all_three = set_a & set_b & set_c

    return {
        "only_a": only_a,
        "only_b": only_b,
        "only_c": only_c,
        "a_and_b": a_and_b,
        "a_and_c": a_and_c,
        "b_and_c": b_and_c,
        "all_three": all_three
    }


def compute_venn_table(a: pd.DataFrame, b: pd.DataFrame, c: pd.DataFrame) -> pd.DataFrame:
    """Visszaadja az elemszámokat egy táblázatban."""
    s = compute_venn_sets(a, b, c)
    data = {
        "csak A": [len(s["only_a"])],
        "csak B": [len(s["only_b"])],
        "csak C": [len(s["only_c"])],
        "A ∩ B": [len(s["a_and_b"])],
        "A ∩ C": [len(s["a_and_c"])],
        "B ∩ C": [len(s["b_and_c"])],
        "A ∩ B ∩ C": [len(s["all_three"])]
    }
    return pd.DataFrame(data)


def plot_and_save_venn(a: pd.DataFrame, b: pd.DataFrame, c: pd.DataFrame, output_dir: str):
    """Létrehozza és elmenti a Venn-diagramot és a táblázatot."""
    s = compute_venn_sets(a, b, c)

    plt.figure(figsize=(8, 8))
    venn3(
        subsets=(
            len(s["only_a"]), len(s["only_b"]), len(s["a_and_b"]),
            len(s["only_c"]), len(s["a_and_c"]), len(s["b_and_c"]),
            len(s["all_three"])
        ),
        set_labels=("Forrás A", "Forrás B", "Forrás C"),
        set_colors=("skyblue", "lightgreen", "lightcoral"),
        alpha=0.8
    )
    plt.title("Adatforrások átfedése – Venn-diagram")
    plt.tight_layout()

    venn_path = os.path.join(output_dir, "venn_diagram.png")
    plt.savefig(venn_path, dpi=300)
    plt.close()
    print(f"Venn-diagram mentve ide: {venn_path}")

    venn_df = compute_venn_table(a, b, c)
    table_path = os.path.join(output_dir, "venn_table.csv")
    venn_df.to_csv(table_path, index=False, encoding="utf-8-sig")
    print(f"Elemszámos Venn-táblázat mentve ide: {table_path}")

    print("\n=== Elemszámos Venn-diagram táblázat ===")
    print(venn_df.to_string(index=False))

