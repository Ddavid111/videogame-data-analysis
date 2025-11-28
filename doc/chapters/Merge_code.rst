Merge Code
=============

A merge-kód felépítése
----------------------

Az alábbi jegyzékek vesznek részt az adathalmazok összefésülésében:

* `merge/sources/ <https://github.com/Ddavid111/videogame-data-analysis/tree/main/merge/sources>`_
  – Az A, B és C forrásadatok beolvasásáért és előtisztításáért felelős modulok.

* `merge/utils/ <https://github.com/Ddavid111/videogame-data-analysis/tree/main/merge/utils>`_
  – Általános segédfüggvények az I/O műveletekhez, tisztításhoz, normalizáláshoz és a merge-lépések támogatásához.

* `merge/visualization/ <https://github.com/Ddavid111/videogame-data-analysis/tree/main/merge/visualization>`_
  – A mergelt adathalmazra épülő hisztogramok, Venn-diagram és összefoglaló ábrák generálása.

* `merge/output/ <https://github.com/Ddavid111/videogame-data-analysis/tree/main/merge/output>`_
  – A futtatás során keletkező kimeneti ábrák (PNG fájlok) gyűjtőmappája.


A merge folyamatot a  
`merge/main.ipynb <https://github.com/Ddavid111/videogame-data-analysis/blob/main/merge/main.ipynb>`_  
notebook vezérli,  
a közös beállításokat pedig a  
`merge/config.py <https://github.com/Ddavid111/videogame-data-analysis/blob/main/merge/config.py>`_  
tartalmazza.

Kiemelt kódrészletek
--------------------

A teljes kódbázis részletes ismertetése nem szükséges, ezért itt csak
néhány érdekesebb és nem triviális megoldást emelek ki. A forráskód 
minden modulja és függvénye részletes docstringgel van ellátva, amelyek 
leírják a funkciók célját és működését.

Az alábbi példák közvetlenül a ``merge/utils`` és ``merge/sources`` modulokból
származnak, és jól bemutatják a merging folyamat összetettebb elemeit.

1. Hiányzó adatok kitöltése forrásprioritással
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A ``fill_missing_from_source`` függvény a merge egyik kulcseleme:  
feladata, hogy a cél-DataFrame (``d``) hiányzó mezőit feltöltse egy
másik forrás (``src``) értékeivel. A kitöltés az ``appid`` alapján történik,
és csak azokat az oszlopokat másolja át, amelyek a két DataFrame-ben
közösek.

.. code-block:: python

    def fill_missing_from_source(d: pd.DataFrame,
                                 src: pd.DataFrame) -> pd.DataFrame:
        src = src.copy()
        src["appid"] = src["appid"].astype(str)

        common_cols = [col for col in src.columns if col in d.columns]

        merged = d.merge(
            src[common_cols],
            on="appid",
            how="left",
            suffixes=("", "_src")
        )

        for col in common_cols:
            if col != "appid":
                merged[col] = merged[col].combine_first(merged[f"{col}_src"])
                merged.drop(columns=[f"{col}_src"], inplace=True)

        return merged

Ez a megoldás biztosítja, hogy a források (C → B → A sorrendben)  
hiányzó mezői fokozatosan és ütközésmentesen kerüljenek kitöltésre
a végső D adatmodellben.


2. Több forrásból származó listák összevonása
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A ``dedup_join`` függvény egyike a merge során használt legfontosabb
segédfüggvényeknek: több listás oszlopot képes duplikátummentesen
összefűzni.

.. code-block:: python

    def dedup_join(*lists):
        combined = []
        for lst in lists:
            if isinstance(lst, list):
                combined.extend(lst)
        return list(dict.fromkeys(combined))

Ezt a függvényt például címkék, műfajok, kategóriák, platformok
összefésülésére használtam.

3. Képernyőképek több forrásból – index-alapú kombinálás
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A ``process_screenshots`` segédfüggvény mindhárom forrásból (A, B, C)
összegyűjti az elérhető képernyőképeket, majd összeállítja a
közös „full” és „thumbnail” oszlopokat.

.. code-block:: python

    def process_screenshots(a, b, c):
        a_thumb = a.set_index("appid").screenshots_thumbs.to_dict()
        b_thumb = b.set_index("appid").screenshots_thumbs.to_dict()
        c_thumb = c.set_index("appid").screenshots_thumbs.to_dict()
        return a_thumb, b_thumb, c_thumb

A merge során a thumbnail-ek összefésülése így történik:

.. code-block:: python

    d["screenshots_thumb"] = d["appid"].map(
        lambda x: c_thumb.get(x, []) + b_thumb.get(x, []) + a_thumb.get(x, [])
    )

Ez tökéletesen mutatja, hogyan kerül érvényesítésre a C → B → A prioritás.

4. Nyelvi mezők tisztítása több lépésben
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Az A, B és C forrásokban szereplő nyelvi mezők (``supported_languages`` és
``full_audio_languages``) rendkívül eltérő formában jelennek meg.  
Előfordulnak:

* HTML tagek (``<br>``, ``<strong>`` stb.),
* BBCode maradványok (``[img]``, ``[b]`` stb.),
* Steam-specifikus kódok (``#lang_xx``),
* egyszerű szöveges felsorolások (vesszővel, pontosvesszővel, perjellel tagolva),
* beágyazott JSON-listák,
* teljesen vegyes, zajos, duplikált formák.

A normalizálási folyamat ezért két külön függvényre épülő tisztítási pipeline-t
alkalmaz: ``clean_language_field_merged`` → ``final_clean_language_list``.

Első lépés: nyers mezők egységesítése
#########################################

A ``clean_language_field_merged`` a nyers bemenetet egy rendezett és
duplikátummentes listává alakítja. A funkció:

* kezeli, ha a mező lista, string vagy JSON-szerű struktúra,
* eltávolítja a HTML- és BBCode-elemeket (``<br>``, ``[img]`` stb.),
* kifejti a több nyelvet tartalmazó sorokat (vessző, pontosvessző, ``/`` alapján),
* eltávolítja a technikai maradványokat (pl. ``#lang_en``),
* kiszűri a teljesen üres vagy zajos elemeket,
* megőrzi az eredeti nyelvneveket, de konzisztens formára hozza azokat.

Példa:

.. code-block:: python

    languages = clean_language_field_merged(raw_languages)

Ha a nyers adat így néz ki::

    "<br>English; Spanish (Latin America); [b]Portuguese[/b]"

akkor a megtisztított lista:

``["English", "Spanish", "Latin America", "Portuguese"]``

Második lépés: szabványosítás és finomhangolt tisztítás
########################################################

A ``final_clean_language_list`` végzi a mélyebb, kontextusfüggő
normalizálást. A függvény:

* eltávolítja a visszamaradt HTML/BBCode fragmentumokat,
* felismeri és egyesíti a több szóból álló nyelvi kifejezéseket  
  (pl. ``Spanish`` + ``Latin America`` → ``Spanish - Latin America``),
* javítja a gyakori elgépeléseket (pl. ``he ew`` → ``Hebrew``),
* eltávolítja a nem nyelv jellegű szemétértékeket,
* lazább, de következetes validációt alkalmaz: csak emberi nyelvre
  hasonlító kifejezéseket hagy meg (legalább 2 karakter, engedélyezett
  írásjelek),
* a végeredményt duplikátummentes listává alakítja.

A pipeline második hívása:

.. code-block:: python

    languages = final_clean_language_list(languages)

A két lépés eredménye egy olyan lista, amely:

* tiszta és egységes nyelvneveket tartalmaz,
* mentes minden technikai és formázási zajtól,
* alkalmas relációs adatbázisba való betöltésre,
* konzisztens az A, B és C források között.

5. B Forrás betöltése és előfeldolgozása
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A **B** forrás (SteamSpy) JSON állományból épül fel, amely egy komplex,
beágyazott szerkezetű objektumgyűjtemény. A betöltéshez egy olyan
függvény készült, amely:

* ellenőrzi a fájl létezését,
* beolvassa a `games.json` tartalmát,
* az egyes játékokhoz tartozó mezőket strukturált rekordokká alakítja,
* külön kezeli a listás mezőket (pl. *packages*, *genres*, *publishers*),
* a *tags* mezőt dict formában normalizálja,
* végül Pandas DataFrame-be rendezi az adatokat.

Az alábbi részlet jól mutatja a JSON → táblás forma átalakításának
lényegét:

.. code-block:: python

   def load_source_b(base_path: str) -> pd.DataFrame:
       file_path = os.path.join(base_path, "games.json")
       with open(file_path, "r", encoding="utf-8") as f:
           dataset = json.load(f)

       records = []
       for appID, game in dataset.items():
           fields = ["name", "release_date", "estimated_owners", "price"]
           record = {key: game.get(key) for key in fields}
           record["appid"] = str(appID)

           list_fields = ["packages", "developers", "publishers", "genres"]
           record.update({f: game.get(f, []) for f in list_fields})

           tags = game.get("tags", {})
           record["tags"] = tags if isinstance(tags, dict) else {}

           records.append(record)

       df_b = pd.DataFrame(records)
       df_b["release_date"] = pd.to_datetime(df_b["release_date"], errors="coerce")

A funkció a későbbi merge-lépésekhez egységes, tisztított és
normalizált struktúrájú DataFrame-et állít elő. A teljes kód a
projektben részletes docstringekkel van ellátva, így minden
függvénynél megtalálható a pontos szerep és működés magyarázata.


Logolás a merge folyamat során
------------------------------

A merge rendszer részletes naplózást (logging) használ annak érdekében,
hogy minden fontosabb lépés és esemény visszakövethető legyen.  
A naplózás segítségével könnyen ellenőrizhető:

* mely forrásfájlok kerültek betöltésre,
* hány rekordot tartalmaztak,
* mely tisztítási és normalizálási lépések futottak le,
* milyen módosítások történtek a merge során (pl. duplikátumok összevonása),
* a teljes folyamat sikeresen lefutott-e.

Az alábbi részlet egy valós futtatás logkimenetéből származik:

.. code-block:: text

    [2025-11-17 20:57:10] INFO: === Starting merge process ===
    [2025-11-17 20:57:50] INFO: Loaded: steam.csv (27075 rows)
    [2025-11-17 20:57:51] INFO: Loaded: steam_description_data_cleaned.csv (27334 rows)
    [2025-11-17 20:57:52] INFO: Loaded: steam_media_data.csv (27332 rows)
    [2025-11-17 20:57:52] INFO: Loaded: steam_support_info.csv (27136 rows)
    [2025-11-17 20:57:53] INFO: Loaded: steamspy_tag_data.csv (29022 rows)
    [2025-11-17 20:57:53] INFO: Loaded: steam_requirements_data.csv (27319 rows)
    [2025-11-17 20:57:55] INFO: SteamSpy tags converted → 28447 appid with tag data
    [2025-11-17 20:57:55] INFO: A source merged: 27075 rows
    [2025-11-17 20:58:00] INFO: A source saved: C:\Users\zalma\merge\A_merged.csv
    [2025-11-17 20:58:12] INFO: B source loaded from JSON: 111452 rows
    [2025-11-17 20:58:25] INFO: B source saved: C:\Users\zalma\merge\B_full.csv
    [2025-11-17 20:58:32] INFO: Loaded: games_march2025_cleaned.csv (89618 rows)
    [2025-11-17 20:58:38] INFO: Loaded: games_march2025_full.csv (94948 rows)
    [2025-11-17 20:58:44] INFO: Loaded: games_may2024_cleaned.csv (83646 rows)
    [2025-11-17 20:58:49] INFO: Loaded: games_may2024_full.csv (87806 rows)
    [2025-11-17 20:58:49] INFO: C source combined: 356018 rows
    [2025-11-17 20:59:27] INFO: C source saved: C:\Users\zalma\merge\C_full.csv
    [2025-11-17 20:59:28] INFO: Merging sources with C→B→A priority...
    [2025-11-17 20:59:52] INFO: Merge complete (112855 rows, 63 columns)
    [2025-11-17 20:59:57] INFO: Normalized thumbnail screenshots for source A (27075 items)
    [2025-11-17 20:59:57] INFO: Normalized thumbnail screenshots for source B (111452 items)
    [2025-11-17 21:00:03] INFO: Normalized thumbnail screenshots for source C (104490 items)
    [2025-11-17 21:00:05] INFO: Normalized movies for source A (25393 items)
    [2025-11-17 21:00:06] INFO: Normalized movies for source B (111452 items)
    [2025-11-17 21:00:10] INFO: Normalized movies for source C (104490 items)
    [2025-11-17 21:01:44] INFO: Combined duplicate tag columns: ['tags_x', 'tags_y'] → kept unified 'tags'
    [2025-11-17 21:01:57] INFO: Dropped redundant column: steamspy_tags
    [2025-11-17 21:02:06] INFO: Cleaned and normalized language field: supported_languages
    [2025-11-17 21:02:14] INFO: Cleaned and normalized language field: full_audio_languages
    [2025-11-17 21:02:25] INFO: Final language cleanup on supported_languages: 542206 → 542160 entries (after filtering).
    [2025-11-17 21:02:29] INFO: Final language cleanup on full_audio_languages: 212743 → 212736 entries (after filtering).
    [2025-11-17 21:02:29] INFO: 41830 rows have identical supported and audio language sets.
    [2025-11-17 21:02:48] INFO: Merged table saved: C:\Users\zalma\merge\merged_master.csv
    [2025-11-17 21:02:48] INFO: Merged master table saved to: C:\Users\zalma\merge\merged_master.csv
    [2025-11-17 21:02:48] INFO: Source summary saved: C:\Users\zalma\merge\source_summary.csv
    [2025-11-17 21:02:48] INFO: Integrity check completed, saved to C:\Users\zalma\merge\integrity_report.csv
    [2025-11-17 21:02:48] INFO: === Generating histograms ===
    [2025-11-17 21:03:11] INFO: === Merge process successfully completed ===

A logolás végigkíséri az egész merge pipeline-t, így a teljes folyamat
átlátható, hibák esetén pedig gyorsan visszakövethető.
