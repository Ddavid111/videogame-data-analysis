Egységes relációs séma normalizálás
===================================

Bevezetés
---------
A "D" séma a korábbi három (A, B, C) sémák összevonásával és egységesítésével jött létre.  
Kiindulási alapként több, különböző forrásból származó CSV-fájl szolgált, amelyek részben eltérő szerkezetűek voltak, illetve eltérő mezőket tartalmaztak.  

A 2024-es és 2025-ös adatfájlok közötti fő különbség, hogy a 2025-ös verzió tartalmazta a
``discount`` mezőt, míg a 2024-es verzió nem.  
A különböző forrásokból érkező táblák összehangolásával egy egységes, teljes és normalizált adatmodell jött létre.

Normalizálás lépései
--------------------

Első normálforma (1NF)
~~~~~~~~~~~~~~~~~~~~~~
- Az eredeti CSV-fájlok több attribútuma nem atomi értékeket tartalmazott
  (pl. ``tags``, ``genres``, ``categories``, ``supported_languages``, ``requirements`` JSON formában).
- 1NF követelménye, hogy minden attribútum csak atomi értéket vehessen fel.
- Az ilyen mezők önálló táblákba kerültek, a kapcsolatok pedig asszociatív táblákban vannak tárolva.

  Példák:
  * ``game_language`` + ``languages`` (nyelvek + audio flag)
  * ``requirements`` (OS + típus szerinti bontás)
  * ``game_tag`` + ``tags`` (címkék súlyozással)
  * ``game_genre`` + ``genres``
  * ``game_category`` + ``categories``
  * ``game_platform`` + ``platforms``
  * ``game_package`` + ``packages``

Második normálforma (2NF)
~~~~~~~~~~~~~~~~~~~~~~~~~
- A ``game`` tábla elsődleges kulcsa az ``appid``.
- A nem a játék alapadatait leíró, de az ``appid``-tól függő adatok külön táblákba kerültek:
  
  * ``description`` – részletes, rövid és "about the game" leírás
  * ``support`` – támogatási adatok (URL, email, weboldal)
  * ``media`` – multimédiás adatok (fejléckép, háttér)
  * ``screenshots`` – képernyőképek
  * ``movies`` – videók
  * ``requirements`` – rendszerkövetelmények (OS, minimum/ajánlott)
  * ``owners`` – tulajdonosi tartomány szöveges formában

Harmadik normálforma (3NF)
~~~~~~~~~~~~~~~~~~~~~~~~~~
- A tranzitív függőségek megszüntetésére az ismétlődő szöveges mezők önálló entitásokba kerültek.
- A sok-sok kapcsolatokat asszociatív táblák kezelik:

  * ``game_language (appid, langid, audio)``  
  * ``game_tag (appid, tagid, weight)``  
  * ``game_genre (appid, genreid)``  
  * ``game_category (appid, catid)``  
  * ``game_platform (appid, platid)``  
  * ``game_developer (appid, devid)``  
  * ``game_publisher (appid, pubid)``  
  * ``game_package (appid, packid)``  

- Ez biztosítja az adatok konzisztenciáját, minimalizálja a redundanciát
  és lehetővé teszi az egyszerű bővíthetőséget.

Végső séma – "D" reláció
-------------------------
A normalizálás eredményeként a **"D" séma** a következő fő relációkból áll:

* ``game`` – játék alapadatai (név, megjelenési dátum, ár, értékelések, játszási idők, metacritic, tulajdonosok, statisztikák)  
* ``description`` – részletes és rövid szöveges leírások  
* ``support`` – támogatási információk  
* ``media`` – multimédiás adatok (fejléckép, háttér)  
* ``screenshots`` – játékhoz tartozó képernyőképek  
* ``movies`` – játékhoz tartozó videók  
* ``requirements`` – rendszerkövetelmények (platform + típus szerinti bontás)  
* ``languages`` – nyelvek (külön audio flag az asszociatív táblában)  
* ``categories`` – kategóriák  
* ``genres`` – műfajok  
* ``tags`` – címkék (súlyozással)  
* ``platforms`` – platformok  
* ``developers`` – fejlesztők  
* ``publishers`` – kiadók  
* ``packages`` – csomagok  

Kapcsolótáblák:

* ``game_language`` – játék–nyelv kapcsolat  
* ``game_tag`` – játék–címke kapcsolat  
* ``game_genre`` – játék–műfaj kapcsolat  
* ``game_category`` – játék–kategória kapcsolat  
* ``game_platform`` – játék–platform kapcsolat  
* ``game_developer`` – játék–fejlesztő kapcsolat  
* ``game_publisher`` – játék–kiadó kapcsolat  
* ``game_package`` – játék–csomag kapcsolat  

Összefoglalás
-------------
A **D relációs séma** az előző A, B és C sémák összevonásából született meg.  
Fő előnyei:

- Egységesítette a különböző CSV-forrásokból származó adatokat  
- Biztosítja az 1NF, 2NF és 3NF követelményeit  
- Megszüntette a redundáns és nem atomi mezőket  
- Kezeli a sok-sok kapcsolatokat asszociatív táblákon keresztül  
- Tartalmaz minden fontos információt a játékokról, bővíthető módon  
- Megkülönbözteti a források közti eltéréseket (pl. ``discount`` csak a 2025-ös adatokban szerepelt)  
