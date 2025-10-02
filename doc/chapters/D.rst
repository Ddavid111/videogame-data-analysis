Egységes relációs séma normalizálás
===================================

Az **"A", "B"** és **"C"** relációs sémák mind különböző forrásokból (külön CSV fájlokból) 
származtak, de hasonló logikai struktúrával rendelkeztek: a játékok alapadatai, 
szöveges leírások, támogatási információk, médiák, kategóriák, nyelvek, címkék, 
fejlesztők, kiadók és értékelések.  

A normalizálási folyamat célja az volt, hogy mindhárom séma redundanciáit 
megszüntessük, és egy **egységes, tiszta adatmodellt** hozzunk létre, 
amely lefedi az összes forrás által biztosított információt.

Normalizálás lépései
--------------------

Első normálforma (1NF)
~~~~~~~~~~~~~~~~~~~~~~
- A denormalizált forrásokban több mező is listajellegű adatot tartalmazott 
  (pl. ``screenshots``, ``tags``, ``categories``, ``genres``, 
  ``supported_languages``).  
- Ezeket külön táblákba bontottam, így minden attribútum atomi értéket vesz fel.  
- Létrejöttek a következő entitások: ``media``, ``description``, 
  ``requirements``, ``categories``, ``genres``, ``languages``, ``tags``.  

Második normálforma (2NF)
~~~~~~~~~~~~~~~~~~~~~~~~~
- A játék fő táblájának elsődleges kulcsa az ``appid``.  
- Az olyan információkat, amelyek csak az ``appid``-tól függnek, de nem a játék 
  többi alapadatát írják le, külön táblákba helyeztem:  

  * ``support`` – támogatási információk  
  * ``media`` – multimédiás adatok (képek, háttér, videók)  
  * ``description`` – szöveges leírások  
  * ``requirements`` – rendszerkövetelmények (JSON mezők szétbontva: OS, típus, leírás)  
  * ``categories`` – kategóriák  
  * ``genres`` – műfajok  
  * ``languages`` – támogatott nyelvek és teljes audio nyelvek  
  * ``developers`` – fejlesztők  
  * ``publishers`` – kiadók  
  * ``tags`` – címkék  

- A több-több kapcsolatokat kapcsolótáblákkal kezeltem:

  * ``game_category (appid, categoryid)``  
  * ``game_genre (appid, genreid)``  
  * ``game_language (appid, languageid, is_audio)``  
  * ``game_developer (appid, developerid)``  
  * ``game_publisher (appid, publisherid)``  
  * ``game_tag (appid, tagid)``  

Harmadik normálforma (3NF)
~~~~~~~~~~~~~~~~~~~~~~~~~~
- A tranzitív függőségeket megszüntettem:  

  * a ``categories``, ``genres``, ``languages``, ``developers``, ``publishers``, 
    ``tags`` táblák önállóan tárolják a megnevezéseket (pl. ``genre_name``)  
  * a kapcsolótáblák kizárólag azonosítókat tartalmaznak, így nincs redundancia,  
  * a ``requirements`` tábla normalizált formában tárolja a JSON-ból 
    származó rendszerkövetelményeket.  

Végső egységes séma
-------------------
A normalizálás eredményeként az **egységes relációs séma** a következő táblákból áll:  

**Fő entitások:**

* ``game`` – játék alapadatai (appid, név, megjelenés dátuma, ár, értékelések, playtime, metacritic, statisztikai mutatók)  
* ``support`` – támogatási információk  
* ``media`` – multimédiás adatok  
* ``description`` – szöveges leírások  
* ``requirements`` – rendszerkövetelmények normalizált formában  
* ``categories`` – kategóriák  
* ``genres`` – műfajok  
* ``languages`` – nyelvek  
* ``developers`` – fejlesztők  
* ``publishers`` – kiadók  
* ``tags`` – címkék  

**Kapcsolótáblák:**

* ``game_category`` – játék–kategória kapcsolat  
* ``game_genre`` – játék–műfaj kapcsolat  
* ``game_language`` – játék–nyelv kapcsolat (jelölve, ha teljes audio támogatás)  
* ``game_developer`` – játék–fejlesztő kapcsolat  
* ``game_publisher`` – játék–kiadó kapcsolat  
* ``game_tag`` – játék–címke kapcsolat  

Összefoglalás
-------------
Az **egységes relációs séma** biztosítja:  

- Az 1NF, 2NF és 3NF követelményeinek teljesülését  
- Az összes forrásból származó információk egységes integrációját  
- Az adatredundancia minimális szintre csökkentését  
- A több-több kapcsolatok kezelését kapcsolótáblákkal  
- A rendszerkövetelmények (requirements) JSON struktúrájának normalizálását  
- A séma könnyű bővíthetőségét és karbantarthatóságát a jövőben  
