===========================================
Hisztogramok és trendvizualizációk
===========================================

Ez a fejezet a videojáték-megjelenések időbeli dinamikáját mutatja be.
Az ábrák a Steam teljes adatbázisából generált statisztikákra épülnek
(1997–2025 májusáig).

Az elemzésben megjelennek:

- éves megjelenésszámok (összesített, érák szerint)
- forráskategóriák szerinti bontások (**A / B / C**)
- műfaji trendek (Top 5)
- növekedési faktorok (log skálán)
- szezonális mintázatok (havi / heti / napi felbontásban)
- év × nap hőtérkép
- logaritmikus trendbecslés és 2026 előrejelzés

Az ábrák minden esetben a következő könyvtárban találhatók:

`merge/output <https://github.com/Ddavid111/videogame-data-analysis/blob/main/merge/output>`_

Összes játék megjelenése évente
-------------------------------------------

.. image:: ../../merge/output/hist_all_years.png
   :align: center
   :alt: Összes játék megjelenése évente
   :class: merge-diagram

Az ábra jól mutatja a 2014 utáni extrém gyors növekedést,
melyet a Steam Direct modell és az indie fejlesztők tömeges megjelenése okozott.
2024-ben érte el a csúcsot, 21 000 feletti megjelenésszámmal.


Játékmegjelenések 2010 előtt
-------------------------------------------

.. image:: ../../merge/output/hist_pre2010.png
   :align: center
   :alt: Megjelenések 2010 előtt
   :class: merge-diagram

A 2010 előtti időszakban még nagyságrendekkel kevesebb cím érkezett:
a kiadói modell dominált, indie fejlesztők alig voltak jelen.


Játékmegjelenések 2010 után
-------------------------------------------

.. image:: ../../merge/output/hist_post2010.png
   :align: center
   :alt: Megjelenések 2010 után
   :class: merge-diagram

A 2014-es váltás után ugrásszerű növekedés indult,
és a 2020–2024 közötti években stabilan 10–20 ezer közötti cím érkezett évente.


Forrás szerinti bontás (**A, B, C kategória**)
-----------------------------------------------

A kategóriák:

- **A dataset**
- **B dataset**
- **C dataset**

A három kategória külön grafikonon is megjelenik.

**A kategória:**

.. image:: ../../merge/output/hist_sources_A.png
   :align: center
   :alt: A kategória évenkénti megjelenései
   :class: merge-diagram

**B kategória:**

.. image:: ../../merge/output/hist_sources_B.png
   :align: center
   :alt: B kategória évenkénti megjelenései
   :class: merge-diagram

**C kategória:**

.. image:: ../../merge/output/hist_sources_C.png
   :align: center
   :alt: C kategória évenkénti megjelenései
   :class: merge-diagram

A **B** és **C** kategória növekedése sokkal szignifikánsabb, mint az **A** kategóriáé.
2025-ben már májusig 2300+ **B** kategóriás megjelenés történt.


Top 5 műfaj időbeli trendje
-------------------------------------------

.. image:: ../../merge/output/hist_genres_top5.png
   :align: center
   :alt: Top 5 műfaj trendje
   :class: merge-diagram

A legnépszerűbb műfajok:

- Indie
- Casual
- Action
- Adventure
- Simulation

Az Indie műfaj toronymagasan vezet.


Éves növekedési faktor (log-skála)
-------------------------------------------

.. image:: ../../merge/output/hist_growth_rates.png
   :align: center
   :alt: Éves növekedési faktor
   :class: merge-diagram

A logaritmikus skála jól mutatja a kiugró éveket (2005, 2014),
illetve a stagnáló vagy visszaeső periódusokat.


Év × nap hőtérkép
-------------------------------------------

.. image:: ../../merge/output/heatmap_year_day.png
   :align: center
   :alt: Év × Nap hőtérkép
   :class: merge-diagram

A hőtérkép látványosan mutatja a publikálási szezonalitást.
2023–2025 között már szinte minden napra jut több tucat megjelenés.


Szezonális mintázatok – havi, heti, napi
-------------------------------------------

**Havi overlay:**

.. image:: ../../merge/output/seasonal_monthly_overlay.png
   :align: center
   :alt: Havi szezonális mintázatok
   :class: merge-diagram

**Heti overlay:**

.. image:: ../../merge/output/seasonal_weekly_overlay.png
   :align: center
   :alt: Heti szezonális mintázatok
   :class: merge-diagram

**Napi overlay:**

.. image:: ../../merge/output/seasonal_daily_overlay.png
   :align: center
   :alt: Napi szezonális mintázatok
   :class: merge-diagram

A napi adatok különösen zajosak, de jól látszik,
hogy a 2020 utáni időszakban extrém mennyiségű cím jelenik meg
szinte minden egyes napon.


2026 előrejelzés (logaritmikus trend alapján)
---------------------------------------------

.. image:: ../../merge/output/forecast_2026_log_modern.png
   :align: center
   :alt: 2026 logaritmikus előrejelzés
   :class: merge-diagram

A modern évek (2014–2024) logaritmikus trendje alapján a 2026-os évre
**~35 789 új játékmegjelenés** várható.

Ez a történelmi adatok alapján reális extrapoláció,
bár a piac telítődése miatt később megtörhet a növekedés.
