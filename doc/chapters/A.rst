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
  * ``genres`` + ``game_genre`` – műfajok és játék–műfaj kapcsolat
  * ``platforms`` + ``game_platform`` – platformok és játék–platform kapcsolat
  * ``categories`` + ``game_category`` – kategóriák és játék–kategória kapcsolat
  * ``screenshots`` és ``movies`` – minden kép vagy videó külön rekordban tárolva
  * ``requirements`` – a rendszerkövetelmények OS és típus (minimum/ajánlott) szerinti bontásban

Második normálforma (2NF)
~~~~~~~~~~~~~~~~~~~~~~~~~
- A ``game`` tábla elsődleges kulcsa az ``appid``.
- Az olyan adatok, amelyek csak az ``appid``-tól függnek, de nem a játék alapadatait írják le,
  külön táblákba kerültek:

  * ``description`` – részletes, rövid és általános leírások
  * ``support`` – támogatási információk (URL, email)
  * ``media`` – fejléckép és háttér
  * ``requirements`` – operációs rendszer és követelménytípus szerinti bontás

Harmadik normálforma (3NF)
~~~~~~~~~~~~~~~~~~~~~~~~~~
- A tranzitív függőségeket megszüntettem:

  * A ``developers`` és ``publishers`` önálló entitások lettek, 
    az ``appid``-hoz kapcsolótáblákon (``game_developer``, ``game_publisher``) keresztül kötődnek.
  * A ``categories``, ``genres``, ``tags``, ``platforms`` táblák külön tárolják a neveket,
    és csak azonosítók szerepelnek a kapcsolatokban.

- Minden több-több kapcsolat kapcsolótáblával van kezelve, így nincs redundancia a szöveges értékekben.

Végső séma – "A" reláció
--------------------------

A normalizálás eredményeként az **"A" séma** a következő főbb táblákból épül fel:

* ``game`` – játék alapadatai
* ``description`` – leírások
* ``support`` – támogatási információk
* ``media`` – médiatartalmak
* ``screenshots`` – képernyőképek
* ``movies`` – előzetesek, videók
* ``requirements`` – rendszerkövetelmények
* ``tags`` – címkék
* ``genres`` – műfajok
* ``platforms`` – platformok
* ``categories`` – kategóriák
* ``publishers`` – kiadók
* ``developers`` – fejlesztők

Kapcsolótáblák
~~~~~~~~~~~~~~
* ``game_tag`` – játék–címke kapcsolat
* ``game_genre`` – játék–műfaj kapcsolat
* ``game_platform`` – játék–platform kapcsolat
* ``game_category`` – játék–kategória kapcsolat
* ``game_publisher`` – játék–kiadó kapcsolat
* ``game_developer`` – játék–fejlesztő kapcsolat


Összefoglalás
-------------

Az **"A" relációs séma** normalizálási lépései biztosítják:

- Az adatredundancia minimális szinten tartását
- A tranzitív függőségek kiküszöbölését
- A listás és JSON mezők felbontását önálló táblákba
- A sémák karbantarthatóságát és bővíthetőségét

Relációs séma diagram
----------------------

.. image:: ../Relational_data_models/A_normalized.svg
   :align: center
   :alt: A relációs séma diagram
   :class: image-group

Dictionary
----------

Az **"A" adathalmaz dictionary-je** az alábbi linken érhető el:

* `A dataset dictionary <https://github.com/Ddavid111/videogame-data-analysis/blob/main/doc/Dictionaries/A_schema_data_dictionary.xlsx>`_