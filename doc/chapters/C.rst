"C" relációs séma normalizálás
================================

Bevezetés
---------

A kiindulópont négy külön CSV-fájl volt:

- ``games_march2025_cleaned``
- ``games_march2025_full``
- ``games_may2024_cleaned``
- ``games_may2024_full``

A ``full`` állományok a teljes, nyers adatokat tartalmazták minden mezővel, míg a 
``cleaned`` változatok előfeldolgozott, tisztított adatokkal rendelkeztek.  
A 2025-ös CSV-kben található egy további mező is (``discount``), amely a 2024-es 
verziókban még nem szerepelt.  

Normalizálás lépései
--------------------

Első normálforma (1NF)
~~~~~~~~~~~~~~~~~~~~~~
- Az eredeti CSV-kben több attribútum nem atomi értékeket tartalmazott 
  (pl. ``screenshots``, ``tags``, ``categories``, ``genres``, 
  ``supported_languages``).  
- Ezeket külön táblákba helyeztem, hogy minden attribútum atomi legyen.  
- Külön entitások jöttek létre: ``media``, ``screenshots``, ``movies``, ``description``, 
  ``categories``, ``genres``, ``languages``, ``platforms``, ``packages``.  

Második normálforma (2NF)
~~~~~~~~~~~~~~~~~~~~~~~~~
- A játék fő táblájának elsődleges kulcsa az ``appid``.  
- Az olyan adatok, amelyek csak az ``appid``-tól függtek, de nem a játék 
  többi jellemzőjét írták le, külön táblákba kerültek:  

  * ``support`` – támogatási információk  
  * ``media`` – fejléckép és egyéb multimédiás tartalmak  
  * ``screenshots`` – képernyőképek  
  * ``movies`` – videók  
  * ``description`` – részletes leírás, rövid leírás, about the game  
  * ``categories`` – játék kategóriák  
  * ``genres`` – műfajok  
  * ``languages`` – támogatott nyelvek és teljes audio nyelvek (külön audio flag)  
  * ``developers`` – fejlesztők  
  * ``publishers`` – kiadók  
  * ``tags`` – címkék  
  * ``platforms`` – támogatott platformok  
  * ``packages`` – játékcsomagok  

- A redundáns szöveges ismétlődéseket megszüntettem úgy, hogy az entitások 
  saját táblákban tárolják a neveket, és csak azonosítók szerepelnek a kapcsolatokban.  

Harmadik normálforma (3NF)
~~~~~~~~~~~~~~~~~~~~~~~~~~
- A tranzitív függőségeket megszüntettem:

  * a ``categories``, ``genres``, ``languages``, ``developers``, ``publishers``, 
    ``tags``, ``platforms``, ``packages`` táblák önállóan tartalmazzák a megnevezéseket  
  * a játék és ezek az entitások közötti több-több kapcsolatot külön asszociatív 
    táblák kezelik  

- Asszociatív táblák:  

  * ``game_category (appid, categoryid)``  
  * ``game_genre (appid, genreid)``  
  * ``game_language (appid, langid, audio)``  
  * ``game_developer (appid, developerid)``  
  * ``game_publisher (appid, publisherid)``  
  * ``game_tag (appid, tagid)``  
  * ``game_platform (appid, platformid)``  
  * ``game_package (appid, packageid)``  

- Így kiküszöböltük az adatredundanciát, és biztosítottuk az adatok konzisztenciáját.  

Végső séma – "C" reláció
-------------------------
A normalizálás eredményeként a **"C" séma** a következő relációkból áll:  

* ``game`` – játék alapadatai (appid, név, dátum, ár, értékelések, playtime, metacritic, statisztikai mutatók, valamint a 2025-ös verziókban a ``discount`` mező)  
* ``support`` – támogatási információk  
* ``media`` – multimédiás adatok  
* ``screenshots`` – képernyőképek  
* ``movies`` – videók  
* ``description`` – szöveges leírások  
* ``categories`` – kategóriák  
* ``genres`` – műfajok  
* ``languages`` – nyelvek  
* ``developers`` – fejlesztők  
* ``publishers`` – kiadók  
* ``tags`` – címkék  
* ``platforms`` – platformok  
* ``packages`` – csomagok  

Kapcsolótáblák:

* ``game_category`` – játék–kategória kapcsolat  
* ``game_genre`` – játék–műfaj kapcsolat  
* ``game_language`` – játék–nyelv kapcsolat (audio flaggel)  
* ``game_developer`` – játék–fejlesztő kapcsolat  
* ``game_publisher`` – játék–kiadó kapcsolat  
* ``game_tag`` – játék–címke kapcsolat  
* ``game_platform`` – játék–platform kapcsolat  
* ``game_package`` – játék–csomag kapcsolat  

Összefoglalás
--------------
A **C relációs séma** eredménye egy egységes, tiszta és normalizált adatmodell, amely:  

- Négy külön CSV redundáns tárolásából egy konzisztens sémát hozott létre  
- Biztosítja az 1NF, 2NF és 3NF követelményeit  
- Kezeli a sok-sok kapcsolatokat asszociatív táblák segítségével  
- Külön táblákban kezeli a listaértékű mezőket (pl. screenshots, nyelvek, platformok, csomagok)  
- Csökkenti az adatredundanciát és megkönnyíti a karbantartást  
- Rugalmasan kezeli a különbséget a 2024-es és 2025-ös adatforrások között  
  (a ``discount`` mező a 2025-ös CSV-kben szerepel, a 2024-esekben nem)  
- Könnyen bővíthető a jövőben további entitásokkal és attribútumokkal  
