A merged tábla felosztása (splitting)
======================================

A split folyamat célja, hogy a ``merged_master.csv`` egyetlen, nagy
táblájából **tematikus, normalizált CSV-fájlokat** hozzon létre.
Minden táblát külön függvény épít fel, és a fájlok a `split/ <https://github.com/Ddavid111/videogame-data-analysis/blob/main/split>`_  könyvtárba
kerülnek mentésre. A kód futása során részletes log készül
(`split_log.txt <https://github.com/Ddavid111/videogame-data-analysis/blob/main/split/split_log.txt>`_ ), amelyben minden művelet nyomon követhető.

A folyamat lépései röviden
--------------------------

A ``main()`` függvény a teljes feldolgozást automatizálja:

1. **A merged_master.csv betöltése**
2. **Minden rész-tábla létrehozása**
3. **CSV-fájlok mentése**
4. **Naplózás (logging)**

Létrehozott táblák
------------------

Az alábbi CSV-fájlok készülnek el a split folyamat során:

* ``game.csv`` – a játékok alapadatai  
* ``description.csv`` – hosszú, rövid leírások, „about” mezők  
* ``media.csv`` – header image + háttérképek  
* ``screenshots.csv`` – teljes és thumbnail képek  
* ``movies.csv`` – max/480p/thumbnail videók  
* ``support.csv`` – support URL + email  
* ``requirements.csv`` – minimum és ajánlott rendszerkövetelmények OS-enként  
* ``platforms.csv`` és ``game_platform.csv`` – Windows/Mac/Linux támogatás  
* ``genres.csv`` és ``game_genre.csv`` – műfajok és kapcsolótábla  
* ``categories.csv`` és ``game_category.csv`` – kategóriák és kapcsolótábla  
* ``packages.csv``, ``sub_package.csv``, ``game_package.csv`` – Steam csomagok  
* ``developers.csv`` és ``game_developer.csv`` – fejlesztők  
* ``publishers.csv`` és ``game_publisher.csv`` – kiadók  
* ``tags.csv`` és ``game_tag.csv`` – címkék súlyokkal  
* ``languages.csv`` – normalizált nyelvlista  
* ``game_subtitles.csv`` és ``game_audio_language.csv`` – felirat + audio nyelvek

A split kód működésének lényege
--------------------------------

A feldolgozás minden résztáblánál ugyanazt az alapelveket követi:

* **csak a releváns oszlopok kiválasztása a master táblából**,  
* **listás mezők normalizálása** (pl. screenshotok, címkék, nyelvek),  
* **szükség esetén ID-k generálása** (pl. ``genreid``, ``tagid``),  
* **kapcsolótáblák létrehozása** many-to-many kapcsolatokhoz,  
* **mentés CSV-be** a ``split/`` mappába.

Ez a struktúra biztosítja, hogy a korábban egyetlen táblában szereplő,
összevont adatállomány teljes mértékben megfeleljen a relációs
adatbázis-normalizálási elveknek és későbbi SQL importálásra alkalmas
legyen.
