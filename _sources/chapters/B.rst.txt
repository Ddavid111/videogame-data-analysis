"B" relációs séma normalizálás
==============================

Normalizálás lépései
--------------------

Első normálforma (1NF)
~~~~~~~~~~~~~~~~~~~~~~
- Az eredeti ``game (games.csv)`` tábla tartalmazott ismétlődő és listajellegű mezőket  
  (pl. ``screenshots``, ``tags``, ``categories``, ``genres``, ``supported_languages``).  
- Ezeket külön táblákba bontottam:

  * ``media``, ``screenshots``, ``movies`` – a képek és videók atomi sorokban tárolva.  
  * ``categories`` és ``game_category`` – minden kategória külön sorban, kapcsolótáblával.  
  * ``genres`` és ``game_genre`` – minden műfaj külön sorban, kapcsolótáblával.  
  * ``tags`` és ``game_tag`` – címkék külön táblában, kapcsolótáblával.  
  * ``languages`` és ``game_language`` – nyelvek külön táblában, ``audio`` flag-gel a teljes audio nyelvek jelzésére.  
  * ``platforms`` és ``game_platform`` – a játék és platform (Windows, Mac, Linux) kapcsolat normalizált formában.  

Második normálforma (2NF)
~~~~~~~~~~~~~~~~~~~~~~~~~
- A játék tábla elsődleges kulcsa az ``appid``.  
- Az olyan adatok, amelyek nem közvetlenül a játék alapadataihoz tartoznak, külön táblákba kerültek:  

  * ``support`` – támogatási információk (support_url, support_email, website).  
  * ``media``, ``screenshots``, ``movies`` – multimédiás elemek.  
  * ``categories``, ``genres``, ``tags``, ``languages``, ``platforms``, ``developers``, ``publishers``.  

- A több-több kapcsolatokat asszociatív táblákkal oldottam meg:  

  * ``game_tag (appid, tagid)``  
  * ``game_genre (appid, genreid)``  
  * ``game_language (appid, langid, audio)``  
  * ``game_developer (appid, devid)``  
  * ``game_publisher (appid, pubid)``  
  * ``game_category (appid, catid)``  
  * ``game_platform (appid, platid)``  

Harmadik normálforma (3NF)
~~~~~~~~~~~~~~~~~~~~~~~~~~
- A tranzitív függőségeket megszüntettem:  

  * A ``tags``, ``genres``, ``languages``, ``developers``, ``publishers``, ``categories``, ``platforms`` táblák külön tárolják a megnevezéseket, így nincs redundancia.  
  * A ``game_language`` táblában az ``audio`` flag oldja meg a ``full_audio_languages`` mezőt.  
  * A platformok (``Windows``, ``Mac``, ``Linux``) normalizálva lettek a ``platforms`` táblába.  

Végső séma – "B" reláció
------------------------
A normalizálás eredményeként a **"B" séma** a következő fő relációkból áll:  

* ``game`` – játék alapadatai (appid, név, dátum, ár, értékelések, playtime, metacritic stb.)  
* ``support`` – támogatási információk  
* ``media`` – képek 
* ``screenshots`` – képernyőfotók  
* ``movies`` – előzetesek, videók  
* ``categories`` – kategória nevek  
* ``genres`` – műfaj nevek  
* ``tags`` – címkék  
* ``languages`` – nyelvek  
* ``platforms`` – platformok  
* ``developers`` – fejlesztők  
* ``publishers`` – kiadók  

Kapcsolótáblák:  

* ``game_tag`` – játék–címke kapcsolat  
* ``game_genre`` – játék–műfaj kapcsolat  
* ``game_language`` – játék–nyelv kapcsolat (``audio`` flag-gel)  
* ``game_developer`` – játék–fejlesztő kapcsolat  
* ``game_publisher`` – játék–kiadó kapcsolat  
* ``game_category`` – játék–kategória kapcsolat  
* ``game_platform`` – játék–platform kapcsolat  

Összefoglalás
--------------
A **B relációs séma** eredménye egy tiszta, normalizált adatmodell, amely:  

- Atomi értékeket tartalmaz (1NF)  
- Megszünteti a részleges függőségeket (2NF)  
- Kiküszöböli a tranzitív függőségeket (3NF)  
- Külön táblákban kezeli a listaértékű mezőket (pl. nyelvek, kategóriák, címkék, műfajok, platformok)  
- A ``full_audio_languages`` információt a ``game_language.audio`` mező tárolja  
- Lehetővé teszi a több-több kapcsolatok kezelését kapcsolótáblákkal  
- Könnyen bővíthető, karbantartható és redukálja az adatredundanciát.  
