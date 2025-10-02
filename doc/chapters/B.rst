"B" relációs séma normalizálás
================================

Normalizálás lépései
--------------------

Első normálforma (1NF)
~~~~~~~~~~~~~~~~~~~~~~
- Az eredeti ``game (games.csv)`` tábla tartalmazott ismétlődő és listajellegű mezőket 
  (pl. ``screenshots``, ``tags``, ``categories``, ``genres``, ``supported_languages``).  
- A ``requirements`` mező JSON struktúrában tárolta a PC, Mac és Linux rendszerkövetelményeket 
  (minimális és ajánlott). Ez nem felelt meg az atomi érték követelményének.  
- Ezeket külön táblákba bontottam:

  * ``media`` – a képek és videók atomi sorokban tárolva.  
  * ``categories`` és ``game_category`` – minden kategória külön sorban, kapcsolótáblával.  
  * ``genres`` és ``game_genre`` – minden műfaj külön sorban, kapcsolótáblával.  
  * ``tags`` és ``game_tag`` – címkék külön táblában, kapcsolótáblával.  
  * ``languages`` és ``game_language`` – nyelvek külön táblában, audio flag-gel.  
  * ``requirements`` – platform + típus (minimális/ajánlott) szintű bontás külön táblában.  

Második normálforma (2NF)
~~~~~~~~~~~~~~~~~~~~~~~~~
- A játék tábla elsődleges kulcsa az ``appid``.  
- Az olyan adatok, amelyek kizárólag ettől a kulcstól függenek, de nem közvetlenül a játék 
  alapadatait írják le, külön táblákba kerültek:  

  * ``support`` – támogatási információk (support_url, support_email, website).  
  * ``media`` – képek, háttér, videók.  
  * ``requirements`` – rendszerkövetelmények OS és típus szerint normalizálva.  
  * ``categories`` – kategóriák a játékhoz kapcsolva.  
  * ``genres`` – műfajok.  
  * ``languages`` – támogatott nyelvek, teljes audio nyelvek.  
  * ``developers`` – fejlesztők.  
  * ``publishers`` – kiadók.  
  * ``tags`` – címkék.  

- A több-több kapcsolatokat asszociatív táblákkal oldottam meg:  

  * ``game_tag (appid, tagid)``  
  * ``game_genre (appid, genreid)``  
  * ``game_language (appid, languageid, audio)``  
  * ``game_developer (appid, developerid)``  
  * ``game_publisher (appid, publisherid)``  
  * ``game_category (appid, categoryid)``  

Harmadik normálforma (3NF)
~~~~~~~~~~~~~~~~~~~~~~~~~~
- A tranzitív függőségeket megszüntettem:  

  * A ``tags``, ``genres``, ``languages``, ``developers`` és ``publishers`` külön 
    táblákban tárolják a megnevezéseket (pl. ``tag_name``, ``genre_name``), így 
    nincs redundancia.  
- A ``requirements`` tábla normalizált formában tartalmazza a JSON mezőből kibontott adatokat 
  (platform, típus, leírás).  
- A játék és ezek az entitások közötti kapcsolatokat kizárólag kapcsolótáblák 
  kezelik, ezzel biztosítva az egyértelműséget.  

Végső séma – "B" reláció
----------------------
A normalizálás eredményeként a **"B" séma** a következő fő relációkból áll:  

* ``game`` – játék alapadatai (appid, név, dátum, ár, értékelések, playtime, metacritic stb.)  
* ``support`` – támogatási információk  
* ``media`` – multimédiás adatok (képek, videók)  
* ``requirements`` – rendszerkövetelmények (OS + típus szinten)  
* ``categories`` – kategória nevek  
* ``genres`` – műfaj nevek  
* ``tags`` – címkék  
* ``languages`` – nyelvek  
* ``developers`` – fejlesztők  
* ``publishers`` – kiadók  

Kapcsolótáblák:  

* ``game_tag`` – játék–címke kapcsolat  
* ``game_genre`` – játék–műfaj kapcsolat  
* ``game_language`` – játék–nyelv kapcsolat (audio flag-gel)  
* ``game_developer`` – játék–fejlesztő kapcsolat  
* ``game_publisher`` – játék–kiadó kapcsolat  
* ``game_category`` – játék–kategória kapcsolat  

Összefoglalás
-------------
A **B relációs séma** eredménye egy tiszta, normalizált adatmodell, amely:  

- Atomi értékeket tartalmaz (1NF)  
- Megszünteti a részleges függőségeket (2NF)  
- Kiküszöböli a tranzitív függőségeket (3NF)  
- Felbontja a JSON típusú ``requirements`` mezőt külön táblára  
- Külön táblákban kezeli a listaértékű mezőket (pl. nyelvek, kategóriák, címkék, műfajok)  
- Lehetővé teszi a több-több kapcsolatok kezelését kapcsolótáblákkal  
- Könnyen bővíthető, karbantartható és redukálja az adatredundanciát.  
