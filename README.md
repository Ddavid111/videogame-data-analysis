# videogame-data-analysis

A Steam az egyik legnagyobb online szolgáltatás és alkalmazásbolt, amely elsődlegesen
videójátékok forgalmazásával foglalkozik. A benne lévő, játékokhoz kapcsolódó adatok
elérhetőek, elemzésre alkalmasak. A diplomamunka célja, hogy különféle statisztikai és gépi
tanulási módszerek alkalmazásával összefüggéseket találjon, következtetéseket vonjon le.
Az elemzésekhez a Python programozási nyelvhez elérhető elemzőeszközök kerülnek
felhasználásra (például: NumPy, pandas). A dolgozathoz tartozó szoftverek, elemzések
Jupyter munkafüzetek formájában készülnek.

-Dataset-ek:

https://www.kaggle.com/datasets/nikdavis/steam-store-games (A)
https://www.kaggle.com/datasets/fronkongames/steam-games-dataset (B)
https://www.kaggle.com/datasets/artermiloff/steam-games-dataset (C)

### Adatok előkészítése

A datasetek méretük miatt nem kerültek feltöltésre a repository-ba, hanem a fenti Kaggle-oldalakról tölthetők le.  
Az elemzések futtathatók **Google Colab** vagy **helyi Jupyter Notebook** környezetben.

- Colab esetén a fájlok elhelyezhetők a Google Drive-ban (pl. `/MyDrive/steam-data/`), és a Drive a következő módon csatolható:
  ```python
  from google.colab import drive
  drive.mount('/content/drive')
  DATA_PATH = '/content/drive/MyDrive/steam-data/'

- Helyi futtatás esetén a datasetek a projekt data/ mappájába kerülhetnek:

    ```python
    DATA_PATH = './data/'

- A notebookok az adatfájlokat ebből a könyvtárból olvassák be, például:

    ```python
    import pandas as pd
    df = pd.read_csv(DATA_PATH + 'steam_games_A.csv')