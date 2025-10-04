"A" relációs séma normalizálása
==================================

Normalizálás lépései
--------------------

Első normálforma (1NF)
~~~~~~~~~~~~~~~~~~~~~~
- Az eredeti CSV-ben több attribútum nem atomi értékeket tartalmazott 
  (pl. több screenshot, több címke, több kategória egyetlen cellában).
- Az 1NF követelménye, hogy minden attribútum oszthatatlan, atomi értéket vegyen fel.
- A listaértékű és összetett attribútumokat külön táblákba helyeztem.

  Például:

  * ``tags`` + ``game_tag`` – címkék és játék–címke kapcsolat
  * ``categories`` + ``game_category`` – kategóriák és játék–kategória kapcsolat
  * ``platforms`` + ``game_platform`` – platformok és játék–platform kapcsolat
  * ``screenshots`` és ``movies`` – minden kép vagy videó külön rekordban tárolva
  * ``requirements`` – a rendszerkövetelmények OS és típus (minimum/ajánlott) szerinti bontásban

Második normálforma (2NF)
~~~~~~~~~~~~~~~~~~~~~~~~~
- A ``game`` tábla elsődleges kulcsa az ``appid``.
- Az olyan adatok, amelyek csak az ``appid``-tól függnek, de nem a játék alapadatait írják le,
  külön táblákba kerültek:

  * ``description`` – részletes, rövid és általános leírások
  * ``support`` – támogatási információk (support URL, email, weboldal)
  * ``media`` – fejléckép és háttér
  * ``requirements`` – operációs rendszer és követelménytípus szerinti bontás

Harmadik normálforma (3NF)
~~~~~~~~~~~~~~~~~~~~~~~~~~
- A tranzitív függőségeket megszüntettem:

  * A ``developers`` és ``publishers`` önálló entitások lettek, 
    az ``appid``-hoz kapcsolótáblákon (``game_developer``, ``game_publisher``) keresztül kötődnek.
  * A ``categories``, ``genres``, ``tags``, ``platforms`` táblák külön tárolják a neveket,
    és csak azonosítók szerepelnek a kapcsolatokban.

- Minden sok–sok kapcsolat kapcsolótáblával van kezelve, így nincs redundancia a szöveges értékekben.

Végső séma – "A" reláció
--------------------------

A normalizálás eredményeként az **"A" séma** a következő főbb táblákból épül fel:

* ``game`` – játék alapadatai
* ``description`` – leírások (részletes, rövid, about the game)
* ``support`` – támogatási információk
* ``media`` – háttér és fejléckép
* ``screenshots`` – képek
* ``movies`` – videók
* ``requirements`` – rendszerkövetelmények OS és típus szerint
* ``categories`` – kategóriák
* ``genres`` – műfajok
* ``tags`` – címkék
* ``platforms`` – platformok
* ``developers`` – fejlesztők
* ``publishers`` – kiadók

Kapcsolótáblák
~~~~~~~~~~~~~~
* ``game_category`` – játék–kategória kapcsolat
* ``game_genre`` – játék–műfaj kapcsolat
* ``game_tag`` – játék–címke kapcsolat
* ``game_platform`` – játék–platform kapcsolat
* ``game_developer`` – játék–fejlesztő kapcsolat
* ``game_publisher`` – játék–kiadó kapcsolat

Összefoglalás
-------------

Az **"A" relációs séma** normalizálási lépései biztosítják:

- Az adatredundancia minimális szinten tartását
- A tranzitív függőségek kiküszöbölését
- A listás és JSON mezők felbontását önálló táblákba
- A sémák karbantarthatóságát és bővíthetőségét
