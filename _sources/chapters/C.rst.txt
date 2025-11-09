"C" relációs séma normalizálás
==============================

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
  ``supported_languages``, ``full_audio_languages``).  
- Ezeket külön táblákba helyeztem, hogy minden attribútum atomi legyen.  
- Külön entitások jöttek létre: ``media``, ``screenshots``, ``movies``, ``description``, 
  ``categories``, ``genres``, ``languages``, ``platforms``, ``packages``.  
- A nyelvi mezők (``supported_languages``, ``full_audio_languages``) két relációra bontva kerültek tárolásra:  

  * ``game_subtitles`` – a játék–nyelv kapcsolat feliratként  
  * ``game_audio_language`` – a játék–nyelv kapcsolat hang (szinkron) formájában  

Második normálforma (2NF)
~~~~~~~~~~~~~~~~~~~~~~~~~
- A játék fő táblájának elsődleges kulcsa az ``appid``.  
- Az olyan adatok, amelyek csak az ``appid``-tól függtek, de nem a játék 
  többi jellemzőjét írták le, külön táblákba kerültek:  

  * ``support`` – támogatási információk (URL, email)  
  * ``media`` – fejléckép  
  * ``screenshots`` – képernyőképek  
  * ``movies`` – előzetesek, videók  
  * ``description`` – részletes, rövid és általános leírások  
  * ``categories`` – kategóriák  
  * ``genres`` – műfajok  
  * ``languages`` – nyelvek (önálló tábla, a megnevezésekkel)  
  * ``developers`` – fejlesztők  
  * ``publishers`` – kiadók  
  * ``tags`` – címkék  
  * ``platforms`` – támogatott platformok  
  * ``packages`` – játékcsomagok (részletesen lásd lejjebb)  

- A redundáns szöveges ismétlődéseket megszüntettem úgy, hogy az entitások 
  saját táblákban tárolják a neveket, és csak azonosítók szerepelnek a kapcsolatokban.  

Harmadik normálforma (3NF)
~~~~~~~~~~~~~~~~~~~~~~~~~~
- A tranzitív függőségeket megszüntettem:

  * a ``categories``, ``genres``, ``languages``, ``developers``, ``publishers``, 
    ``tags``, ``platforms``, ``packages`` táblák önállóan tartalmazzák a megnevezéseket  
  * a játék és ezek az entitások közötti több-több kapcsolatot külön asszociatív 
    táblák kezelik  

- A csomagstruktúra három szinten valósul meg:  

  * ``game_package (appid, packid)`` – a játék és csomag közötti kapcsolat  
  * ``packages (packid, title, description)`` – a csomag alapadatai  
  * ``sub_package (packid, sub_text, price)`` – az adott csomag al-elemei és ára  

- Asszociatív táblák:  

  * ``game_category (appid, categoryid)``  
  * ``game_genre (appid, genreid)``  
  * ``game_subtitles (appid, languageid)``  
  * ``game_audio_language (appid, languageid)``  
  * ``game_developer (appid, developerid)``  
  * ``game_publisher (appid, publisherid)``  
  * ``game_tag (appid, tagid)``  
  * ``game_platform (appid, platformid)``  
  * ``game_package (appid, packid)``  

- Így kiküszöböltem az adatredundanciát, és biztosítottam az adatok konzisztenciáját.  

Végső séma – "C" reláció
-------------------------
A normalizálás eredményeként a **"C" séma** a következő relációkból áll:  

* ``game`` – játék alapadatai (appid, név, dátum, ár, értékelések, valamint a 2025-ös verziókban a ``discount`` mező)  
* ``support`` – támogatási információk  
* ``media`` – fejléckép  
* ``screenshots`` – képernyőképek  
* ``movies`` – előzetesek, videók  
* ``description`` – leírások  
* ``tags`` – címkék 
* ``genres`` – műfajok 
* ``platforms`` – platformok  
* ``categories`` – kategóriák  
* ``publishers`` – kiadók 
* ``developers`` – fejlesztők 
* ``languages`` – nyelvek (egyedi név)
* ``packages`` – csomagok (alap adatok)  
* ``sub_package`` – csomag al-elemei (leírás és ár)  

Kapcsolótáblák:

* ``game_tag`` – játék–címke kapcsolat  
* ``game_genre`` – játék–műfaj kapcsolat 
* ``game_platform`` – játék–platform kapcsolat 
* ``game_category`` – játék–kategória kapcsolat  
* ``game_publisher`` – játék–kiadó kapcsolat  
* ``game_developer`` – játék–fejlesztő kapcsolat 
* ``game_audio_language`` – játék–hangnyelv kapcsolat   
* ``game_subtitles`` – játék–felirat kapcsolat
* ``game_package`` – játék–csomag kapcsolat  

Összefoglalás
-------------
A **C relációs séma** eredménye egy egységes, tiszta és normalizált adatmodell, amely:  

- Négy külön CSV redundáns tárolásából egy konzisztens sémát hozott létre  
- Biztosítja az 1NF, 2NF és 3NF követelményeit  
- Külön kezeli a feliratokat (``game_subtitles``) és a hangnyelveket (``game_audio_language``)  
- Kezeli a több-több kapcsolatokat asszociatív táblák segítségével  
- Normalizáltan kezeli a csomagokat három szinten: játék–csomag, csomag–adat, csomag–alrész  
- Csökkenti az adatredundanciát és megkönnyíti a karbantartást  
- Rugalmasan kezeli a különbséget a 2024-es és 2025-ös adatforrások között  
  (a ``discount`` mező a 2025-ös CSV-kben szerepel, a 2024-esekben nem)  
- Könnyen bővíthető a jövőben további entitásokkal és attribútumokkal  
