# =========================================
# IMPORTS
# =========================================
import os
import io
import re
import pandas as pd
from bs4 import BeautifulSoup


# =========================================
# HELPER FUNCTIONS
# =========================================
def read_and_fix_multiline_csv(path: str) -> io.StringIO:
    """
    Beolvassa a CSV-t, és kijavítja azokat a sorokat, amelyek
    idézőjelek miatt több sorban vannak.
    Visszatér egy StringIO objektummal, amely egyetlen,
    egységesített CSV-t tartalmaz.
    """
    lines, buf, quote_count = [], [], 0
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.rstrip("\r\n")
            buf.append(line)
            quote_count += len(re.findall(r'(?<!\\)"', line))
            if quote_count % 2 == 0:
                lines.append(" ".join(buf))
                buf, quote_count = [], 0
        if buf:
            lines.append(" ".join(buf))
    return io.StringIO("\n".join(lines))


def clean_html_text(x: str) -> str:
    """
    Eltávolítja a HTML tageket és normalizálja a szöveget.
    """
    if not isinstance(x, str) or not x.strip():
        return ""
    if "<" in x and ">" in x:
        soup = BeautifulSoup(x, "html.parser")
        text = soup.get_text(" ", strip=True)
    else:
        text = x
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def strip_html(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """
    Megtisztítja a megadott oszlopokat a HTML tagektől.
    """
    for col in cols:
        if col in df.columns:
            df[col] = df[col].astype(str).apply(clean_html_text)
    return df


# =========================================
# CORE PROCESSING FUNCTION
# =========================================
def process_description_data(raw_path: str, clean_path: str,
                             desc_cols: list[str]) -> pd.DataFrame:
    """
    Beolvassa a Steam leírásos CSV-t, kijavítja a hibás sorokat,
    eltávolítja a HTML tageket és menti a megtisztított adatokat.
    """
    buffer = read_and_fix_multiline_csv(raw_path)
    df = pd.read_csv(
        buffer,
        engine="python",
        quotechar='"',
        on_bad_lines="skip"
    )

    if "steam_appid" in df.columns and "appid" not in df.columns:
        df.rename(columns={"steam_appid": "appid"}, inplace=True)

    df = strip_html(df, desc_cols)

    if "appid" in df.columns:
        df["appid"] = df["appid"].astype(str).str.strip()
        df.drop_duplicates(subset="appid", inplace=True)
        df.reset_index(drop=True, inplace=True)

    os.makedirs(os.path.dirname(clean_path), exist_ok=True)
    df.to_csv(clean_path, index=False, encoding="utf-8")

    return df


# =========================================
# MAIN FUNCTION
# =========================================
def main():
    """
    A Steam description CSV feldolgozását végzi el:
    - beolvasás
    - HTML tisztítás
    - mentés
    """
    base_path = r"C:\Users\zalma"
    raw_path = os.path.join(base_path, "A", "steam_description_data.csv")
    clean_filename = "steam_description_data_cleaned.csv"
    clean_path = os.path.join(base_path, "A", clean_filename)
    desc_cols = ["detailed_description", "about_the_game", "short_description"]
    df = process_description_data(raw_path, clean_path, desc_cols)

    print(f"Normalizált leírás mentve ide: {clean_path}")
    print(f"Rekordok száma: {len(df)} | Oszlopok száma: {len(df.columns)}")
    print(df.head(5)[['appid', 'short_description']])
