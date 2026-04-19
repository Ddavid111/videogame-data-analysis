Bevezetés
=========

A dokumentáció célja, hogy bemutassa az adatelemzési és
adat-előkészítési folyamat fő lépéseit, valamint az ezekhez tartozó
munkafolyamatokat és eredményeket. A következő fő részek kerülnek
bemutatásra:

* :doc:`Az adathalmazok (A, B, C) külön-külön történő vizsgálata  <Data_exploration>`
  
  Mindegyik datasetet önálló Jupyter munkafüzetben elemeztem, ahol
  áttekintettem az adatok szerkezetét, statisztikáit, minőségét és
  alapvető mintázatait.

* :doc:`Normalizálási folyamat, relációs sémák és adatdictionary-k elkészítése <Data_preparation>`

  Az **A, B és C** adathalmazok esetében először elkészítettem a
  normalizálási folyamat részletes leírását, majd ezek alapján
  felrajzoltam a teljes relációs sémákat, és összeállítottam az
  adathalmazokhoz tartozó adatdictionary-ket. Ezek a dokumentumok
  bemutatják a táblák szerkezetét, a mezők szerepét, adattípusait és
  az adatok közötti kapcsolatokat.

  Ezt követően elkészítettem a **D adathalmaz** normalizálási folyamatát is,
  amely az **A, B és C összevont, egységesített adathalmazából**
  jött létre. A D datasethez szintén felrajzoltam a teljes relációs sémát, összeállítottam az
  adatdictionary-t, majd létrehoztam a normalizált adatbázist, és összeírtam több alapvető
  SQL-lekérdezést, amelyek a struktúra ellenőrzését és a későbbi
  feldolgozási lépéseket támogatják.
  
* :doc:`Adathalmazok összefésülése (merging) <Merge>`

  Rögzítettem a merge-folyamatot egy ábrával és kódrészletekkel.
  Néhány komplikáltabb implementációs részlet külön is ismertetésre kerül.

* :doc:`Elemzések a merged tábláról <Visualization>`  
  
  A létrehozott egyesített adatállományon további elemzéseket
  készítettem, többek között hisztogramokat, Venn-diagramot,
  forrás-eloszlási összegzést és integritásvizsgálatot.

* :doc:`A merged tábla felosztása <Split>`  
  
  A teljes összevont adathalmazt végül kisebb, tematikus részekre
  bontottam további feldolgozás és felhasználás céljából.

A fenti fejezetek részletesen ismertetik a munkafolyamatot az
alapadatok megismerésétől kezdve egészen a végső, feldarabolt és
továbbhasznosítható adatszerkezetig.
