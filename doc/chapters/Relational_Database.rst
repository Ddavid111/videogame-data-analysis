A relációs séma normalizálás
============================

Bevezetés
---------
Ez a dokumentáció az **"A", "B", "C" relációs séma** normalizálási folyamatát mutatja be.  
Az eredeti (denormalizált) struktúra egy nagy táblában tartalmazta az összes 
játékhoz kapcsolódó információt mind három esetben: játék adatok, leírások, médiák, támogatási 
információk, rendszerkövetelmények és címkék.  

A normalizálás célja, hogy az adatokat redundanciamentesen, konzisztensen és 
hatékonyan tároljuk. Az alábbiakban lépésenként bemutatom, hogyan jutottam 
el a **"A", "B", "C"** séma végső formájáig.

