"C" relációs séma normalizálás
================================

Bevezetés
---------
 
A kiindulópont négy külön CSV-fájl volt:

- ``games_march2025_cleaned``
- ``games_march2025_full``
- ``games_may2024_cleaned``
- ``games_may2024_full``

Normalizálás lépései
--------------------

Első normálforma (1NF)
~~~~~~~~~~~~~~~~~~~~~~
- Az eredeti CSV-kben több attribútum nem atomi értékeket tartalmazott 
  (pl. ``screenshots``, ``tags``, ``categories``, ``genres``, 
  ``supported_languages``).  
- A ``requirements`` mező JSON formátumban tárolta a PC, Mac és Linux rendszerkövetelményeket 
  (minimális és ajánlott), ami szintén megsértette az 1NF szabályait.  
- Ezeket külön táblákba helyeztem, hogy minden attribútum atomi legyen.  
- Külön entitások jöttek létre: ``media``, ``description``, ``categories``, 
  ``genres``, ``languages``, ``requirements``.  

Második normálforma (2NF)
~~~~~~~~~~~~~~~~~~~~~~~~~
- A játék fő táblájának elsődleges kulcsa az ``appid``.  
- Az olyan adatok, amelyek csak az ``appid``-tól függtek, de nem a játék 
  többi jellemzőjét írták le, külön táblákba kerültek:  

  * ``support`` – támogatási információk  
  * ``media`` – képek, videók, fejléckép  
  * ``description`` – részletes leírás, rövid leírás, about the game  
  * ``requirements`` – rendszerkövetelmények (platform + típus szerint, pl. minimum/ajánlott)  
  * ``categories`` – játék kategóriák  
  * ``genres`` – műfajok  
  * ``languages`` – támogatott nyelvek és teljes audio nyelvek (külön audio flag)  
  * ``developers`` – fejlesztők  
  * ``publishers`` – kiadók  
  * ``tags`` – címkék  

- A redundáns szöveges ismétlődéseket megszüntettem úgy, hogy az entitások 
  saját táblákban tárolják a neveket, és csak azonosítók szerepelnek a kapcsolatokban.  

Harmadik normálforma (3NF)
~~~~~~~~~~~~~~~~~~~~~~~~~~
- A tranzitív függőségeket megszüntettem:

* a ``categories``, ``genres``, ``languages``, ``developers``, ``publishers``, 
  ``tags`` táblák önállóan tartalmazzák a megnevezéseket (pl. ``genre_name``)
* a játék és ezek az entitások közötti több-több kapcsolatot külön asszociatív 
  táblák kezelik
* a ``requirements`` tábla normalizált formában tárolja a JSON-ból származó adatokat 
  (appid, OS, típus, leírás)


- Asszociatív táblák:  

  * ``game_category (appid, categoryid)``  
  * ``game_genre (appid, genreid)``  
  * ``game_language (appid, languageid, is_audio)``  
  * ``game_developer (appid, developerid)``  
  * ``game_publisher (appid, publisherid)``  
  * ``game_tag (appid, tagid)``  

- Így kiküszöböltük az adatredundanciát, és biztosítottuk az adatok konzisztenciáját.  

Végső séma – "C" reláció
-------------------------
A normalizálás eredményeként a **"C" séma** a következő relációkból áll:  

* ``game`` – játék alapadatai (appid, név, dátum, ár, értékelések, playtime, metacritic, statisztikai mutatók)  
* ``support`` – támogatási információk  
* ``media`` – multimédiás adatok  
* ``description`` – szöveges leírások  
* ``requirements`` – rendszerkövetelmények (platform + típus szerint normalizálva)  
* ``categories`` – kategóriák  
* ``genres`` – műfajok  
* ``languages`` – nyelvek  
* ``developers`` – fejlesztők  
* ``publishers`` – kiadók  
* ``tags`` – címkék  

Kapcsolótáblák:

* ``game_category`` – játék–kategória kapcsolat  
* ``game_genre`` – játék–műfaj kapcsolat  
* ``game_language`` – játék–nyelv kapcsolat (audio flaggel)  
* ``game_developer`` – játék–fejlesztő kapcsolat  
* ``game_publisher`` – játék–kiadó kapcsolat  
* ``game_tag`` – játék–címke kapcsolat  

Összefoglalás
-------------
A **C relációs séma** eredménye egy egységes, tiszta és normalizált adatmodell, amely:  

- Négy külön CSV redundáns tárolásából egy konzisztens sémát hozott létre  
- Biztosítja az 1NF, 2NF és 3NF követelményeit  
- Kezeli a sok-sok kapcsolatokat asszociatív táblák segítségével  
- Felbontja a JSON típusú ``requirements`` mezőt külön táblára  
- Külön táblákban kezeli a listaértékű mezőket (pl. screenshots, nyelvek)  
- Csökkenti az adatredundanciát és megkönnyíti a karbantartást  
- Könnyen bővíthető a jövőben további entitásokkal és attribútumokkal  
