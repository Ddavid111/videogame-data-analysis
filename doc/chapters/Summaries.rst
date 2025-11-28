Source Summary és Integritásvizsgálat
=====================================

Ebben a fejezetben két olyan elemző funkció kerül bemutatásra, amelyek
a teljesen összefésült *D adatmodell* minőségének és forráseloszlásának
áttekintését szolgálják:

1. **Forrásonkénti rekordmegoszlás** (source summary)
2. **Adatintegritás-ellenőrzés** (integrity validation)


1. Forrásonkénti rekordösszesítő (source summary)
-------------------------------------------------

A merged master táblában minden sorhoz tartozik egy ``sources`` mező,
amely azt jelzi, hogy az adott rekord melyik eredeti datasetből
(A, B vagy C) származik. A következő függvény egy részletes
összesítőt készít:

* hány rekord érkezett csak A-ból,
* csak B-ből,
* csak C-ből,
* illetve ezek különböző kombinációiból (pl. “A,B”, “B,C”, “A,B,C”).

Az eredményt egy jól áttekinthető CSV táblázatba is elmenti.

A generált állomány itt érhető el:

`source_summary.csv <https://github.com/Ddavid111/videogame-data-analysis/blob/main/merge/source_summary.csv>`_ — *Forrásonkénti rekordmegoszlás*


.. code-block:: python

    def save_source_summary(d: pd.DataFrame, output_dir: str):

        summary = d["sources"].value_counts().reset_index()
        summary.columns = ["forrás_kombináció", "rekordok_száma"]

        summary["tartalmaz_A"] = summary["forrás_kombináció"].str.contains("A")
        summary["tartalmaz_B"] = summary["forrás_kombináció"].str.contains("B")
        summary["tartalmaz_C"] = summary["forrás_kombináció"].str.contains("C")

        output_file = os.path.join(output_dir, "source_summary.csv")
        summary.to_csv(output_file, index=False, encoding="utf-8-sig")

        logging.info(f"Source summary saved: {output_file}")
        print(summary.to_string(index=False))


Ez az összesítő fontos szerepet játszik annak megértésében, hogy
milyen mértékben fedik egymást a forrásadatok, illetve mennyire
egyensúlyos az A–B–C hozzájárulás a végső D táblában.



2. Adatintegritás-ellenőrzés
----------------------------

Az integritásvizsgálat célja, hogy feltárja a leggyakoribb adatminőségi
problémákat a merged táblában. A függvény a következő ellenőrzéseket
végzi el:

* duplikált appid értékek,  
* hiányzó appid értékek,  
* hiányzó játéknevek,  
* hiányzó forrásjelölés,  
* érvénytelen dátumformátumok a `release_date` mezőben.

Az eredmény egy külön CSV jelentésben kerül mentésre.

`source_summary.csv <https://github.com/Ddavid111/videogame-data-analysis/blob/main/merge/source_summary.csv>`_ — *Integritásvizsgálati összesítő*


.. code-block:: python

    def validate_integrity(d: pd.DataFrame, output_dir: str):

        results = []

        results.append({
            "ellenőrzés": "Duplikált appid-ek",
            "hibák_száma": d["appid"].duplicated().sum()
        })

        results.append({
            "ellenőrzés": "Hiányzó appid-ek",
            "hibák_száma": d["appid"].isna().sum()
        })

        if "name" in d.columns:
            results.append({
                "ellenőrzés": "Hiányzó játéknevek",
                "hibák_száma": d["name"].isna().sum()
            })

        if "sources" in d.columns:
            results.append({
                "ellenőrzés": "Hiányzó forrásjelölés",
                "hibák_száma": (d["sources"] == "").sum()
            })

        if "release_date" in d.columns:
            invalid = pd.to_datetime(d["release_date"], errors="coerce").isna().sum()
            results.append({
                "ellenőrzés": "Érvénytelen release_date",
                "hibák_száma": invalid
            })

        integrity_df = pd.DataFrame(results)

        output_file = os.path.join(output_dir, "integrity_report.csv")
        integrity_df.to_csv(output_file, index=False, encoding="utf-8-sig")

        logging.info(f"Integrity check completed, saved to {output_file}")
        print(integrity_df.to_string(index=False))


Mindkét ellenőrzés a merged tábla minőségét segít értékelni, és
kulcsfontosságú a normalizálási lépések biztonságos végrehajtásához.
