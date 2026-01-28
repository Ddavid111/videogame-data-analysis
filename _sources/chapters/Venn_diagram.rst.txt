Venn-diagram – Források átfedésének vizsgálata
==============================================

A három forrásadat (A, B, C) közötti átfedést egy **Venn-diagram** szemlélteti, 
amely megmutatja, hogy mely appID-k találhatók meg kizárólag egy adott 
adatforrásban, illetve melyek vannak jelen több forrás metszetében is.

.. image:: ../../merge/venn_diagram.png
   :align: center
   :alt: Források átfedése – Venn-diagram
   :class: merge-diagram


Működés
-------

A Venn-diagram létrehozását az alábbi három lépés valósítja meg:

1. **Halmazok kiszámítása appid alapján**

   A ``compute_venn_sets`` függvény mindhárom forráshoz (A, B, C) külön 
   appID-halmazt készít, majd ezek alapján meghatározza:

   * csak A-ban szereplő ID-ket,
   * csak B-ben szereplő ID-ket,
   * csak C-ben szereplő ID-ket,
   * a páronkénti metszeteket (A∩B, A∩C, B∩C),
   * valamint a mindhárom forrásban megtalálható rekordokat.

   .. code-block:: python

      set_a = set(a["appid"].astype(str))
      set_b = set(b["appid"].astype(str))
      set_c = set(c["appid"].astype(str))

      only_a = set_a - set_b - set_c
      a_and_b = (set_a & set_b) - set_c
      all_three = set_a & set_b & set_c


2. **Elemszámok táblázatos előállítása**

   A ``compute_venn_table`` a fenti halmazok elemszámaiból egy jól áttekinthető 
   Pandas DataFrame-et készít, amely CSV-formátumban is elmentésre kerül:

   .. code-block:: python

      data = {
          "csak A": [len(s["only_a"])],
          "csak B": [len(s["only_b"])],
          "csak C": [len(s["only_c"])],
          "A ∩ B": [len(s["a_and_b"])],
          "A ∩ C": [len(s["a_and_c"])],
          "B ∩ C": [len(s["b_and_c"])],
          "A ∩ B ∩ C": [len(s["all_three"])]
      }


3. **A Venn-diagram megrajzolása és mentése**

   A ``plot_and_save_venn`` függvény a *matplotlib_venn* csomaggal rajzolja meg a diagramot, 
   az elemszámokat pedig a megfelelő körökben jeleníti meg.

   .. code-block:: python

      venn3(
          subsets=(
              len(s["only_a"]), len(s["only_b"]), len(s["a_and_b"]),
              len(s["only_c"]), len(s["a_and_c"]), len(s["b_and_c"]),
              len(s["all_three"])
          ),
          set_labels=("Forrás A", "Forrás B", "Forrás C")
      )

   A diagram a ``merge/venn_diagram.png`` fájlba kerül mentésre, 
   míg az elemszámos táblázat `venn_table.csv <https://github.com/Ddavid111/videogame-data-analysis/blob/main/merge/venn_table.csv>`_ formában is elérhető.
