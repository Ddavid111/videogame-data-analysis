"A" relációs séma normalizálása
==================================

Normalizálás lépései
--------------------

Első normálforma (1NF)
~~~~~~~~~~~~~~~~~~~~~~
- A denormalizált tábla redundáns, ismétlődő mezőket tartalmazott
  (pl. több screenshot, több tag vagy kategória egy sorban).
- 1NF követelménye, hogy minden attribútum atomi értéket vegyen fel.
- Ennek érdekében a komplex és listaértékű mezőket külön táblákba bontottam.

  Például:
  
  * ``tags`` – a címkék önálló entitásba kerültek
  * ``game_tag`` – a játék–címke kapcsolat külön asszociatív tábla
  * ``categories`` és ``game_category`` – kategóriák normalizálása
  * ``platforms`` és ``game_platform`` – platformok normalizálása
  * ``owners_range`` – a tulajdonosi tartomány külön mezőkre bontva (min, max)
  * ``screenshots`` és ``movies`` – minden média URL külön rekordban tárolódik
  * ``requirements`` – az eredeti JSON mezők felbontva soronként, 
    OS + minimum/recommended bontással

Második normálforma (2NF)
~~~~~~~~~~~~~~~~~~~~~~~~~
- 2NF feltétele, hogy minden nem-kulcs attribútum teljes mértékben függjön
  az elsődleges kulcstól.
- A ``game`` tábla elsődleges kulcsa az ``appid``.
- A leírás, támogatás, média és rendszerkövetelmény adatok nem a játék
  alapadataitól, hanem magától az ``appid``-tól függnek.
- Ezért külön táblákba kerültek:
  
  * ``description`` – részletes, rövid és általános leírás
  * ``support`` – támogatási információk (weboldal, email, URL)
  * ``media`` – képek, háttér és videók
  * ``requirements`` – platformonkénti rendszerkövetelmények

Harmadik normálforma (3NF)
~~~~~~~~~~~~~~~~~~~~~~~~~~
- 3NF követelménye, hogy ne legyen tranzitív függőség.
- A fejlesztők és kiadók adatai ismétlődhettek volna,
  ezért külön táblába kerültek:
  
  * ``developers`` + ``game_developer``
  * ``publishers`` + ``game_publisher``

- A címkék, kategóriák és platformok is külön azonosítót kaptak,
  így nem kell szöveges mezőket ismételni a táblákban.
- Minden sok-sok kapcsolat kapcsolótáblával van kezelve.

Végső séma – "A" reláció
-----------------------

A normalizálás eredményeként az **"A" séma** a következő relációkból áll:

* ``game`` – játék alapadatai
* ``description`` – részletes leírások
* ``support`` – támogatási információk
* ``media`` – alap médiaadatok
* ``screenshots`` – játékhoz tartozó képek
* ``movies`` – játékhoz tartozó videók
* ``requirements`` – platformonkénti minimum/ajánlott követelmények
* ``owners_range`` – tulajdonosok számtartománya
* ``categories`` – kategóriák
* ``genres`` – műfajok
* ``tags`` – címkék
* ``platforms`` – platformok
* ``developers`` – fejlesztők
* ``publishers`` – kiadók

Kapcsolótáblák:  

* ``game_category`` – játék–kategória kapcsolat
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
