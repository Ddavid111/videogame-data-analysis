#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# ======== IMPORTOK ========
import os
import logging
import pandas as pd

# ======== SOURCE SUMMARY ========
def save_source_summary(D: pd.DataFrame, output_dir: str):
    """
    Összesítő táblázatot készít arról, hogy hány rekord származik
    csak A-ból, csak B-ből, csak C-ből, illetve ezek kombinációiból.
    Az eredményt CSV-be menti és ki is írja a konzolra.
    """
    if "sources" not in D.columns:
        logging.warning("A 'sources' oszlop nem található a merged táblában.")
        return

    summary = D["sources"].value_counts().reset_index()
    summary.columns = ["forrás_kombináció", "rekordok_száma"]

    summary["tartalmaz_A"] = summary["forrás_kombináció"].str.contains("A", regex=False)
    summary["tartalmaz_B"] = summary["forrás_kombináció"].str.contains("B", regex=False)
    summary["tartalmaz_C"] = summary["forrás_kombináció"].str.contains("C", regex=False)

    output_file = os.path.join(output_dir, "source_summary.csv")
    summary.to_csv(output_file, index=False, encoding="utf-8-sig")

    logging.info(f"Source summary saved: {output_file}")
    print("\n=== Forrásonkénti rekordösszesítő táblázat ===")
    print(summary.to_string(index=False))

# ======== INTEGRITY VALIDATION ========
def validate_integrity(D: pd.DataFrame, output_dir: str):
    """
    Adatintegritás-ellenőrzés: duplikált appid, hiányzó értékek, típushibák stb.
    Eredményt logolja és CSV-be menti.
    """
    results = []

    dup_count = D["appid"].duplicated().sum()
    results.append({"ellenőrzés": "Duplikált appid-ek", "hibák_száma": dup_count})

    na_appid = D["appid"].isna().sum()
    results.append({"ellenőrzés": "Hiányzó appid-ek", "hibák_száma": na_appid})

    if "name" in D.columns:
        na_name = D["name"].isna().sum()
        results.append({"ellenőrzés": "Hiányzó játéknevek", "hibák_száma": na_name})

    if "sources" in D.columns:
        na_sources = (D["sources"] == "").sum()
        results.append({"ellenőrzés": "Hiányzó forrásjelölés", "hibák_száma": na_sources})

    if "release_date" in D.columns:
        invalid_dates = pd.to_datetime(D["release_date"], errors="coerce").isna().sum()
        results.append({"ellenőrzés": "Érvénytelen release_date", "hibák_száma": invalid_dates})

    integrity_df = pd.DataFrame(results)
    output_file = os.path.join(output_dir, "integrity_report.csv")
    integrity_df.to_csv(output_file, index=False, encoding="utf-8-sig")

    logging.info(f"Integrity check completed, saved to {output_file}")
    print("\n=== Integritás ellenőrzési összesítő ===")
    print(integrity_df.to_string(index=False))

