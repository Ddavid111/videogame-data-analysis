# ======== IMPORTOK ========
import re
import ast
import html
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import logging


# ======== CLEANING FUNCTIONS ========
def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizálja a DataFrame oszlopneveit: levágja a szóközöket,
    kisbetűssé alakítja, és helyettesíti a szóközöket és kötőjeleket
    alulvonással.
    """
    try:
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("-", "_")
        )
        return df
    except Exception as e:
        logging.error(f"Hiba az oszlopnevek tisztítása közben: {e}")
        return df


def clean_language_field_merged(val):
    """
    Normalizálja a supported_languages / full_audio_languages mezőt:
    - Tisztítja a HTML-, BBCode- és Steam-maradványokat
    - Szétbontja az összefűzött nyelveket (, ; szóköz)
    - Egyesíti az egyszerű HTML-tisztítást és a nyelvnév normalizálást
    """
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return []

    if isinstance(val, (list, tuple, np.ndarray)):
        raw_items = [str(v).strip() for v in val if str(v).strip()]
    else:
        val_str = str(val).strip()
        if not val_str:
            return []
        try:
            parsed = ast.literal_eval(val_str)
            if isinstance(parsed, list):
                raw_items = [str(v).strip() for v in parsed if v]
            else:
                raw_items = [val_str]
        except Exception:
            raw_items = [val_str]

    cleaned = []
    for x in raw_items:
        x = html.unescape(x)
        x = re.sub(r"<[^>]+>", " ", x)
        x = re.sub(r"&lt;/?\w+&gt;", " ", x)
        x = re.sub(r"&nbsp;", " ", x)
        x = re.sub(r"#lang[_\-]?", "", x, flags=re.IGNORECASE)
        x = re.sub(r"\[/?[^\]]+\]", "", x)
        x = re.sub(r"&[a-z]+;", " ", x)
        x = re.sub(r"\s+", " ", x).strip()
        if x:
            cleaned.extend(re.split(r"[,;/]", x))

    cleaned = [c.strip() for c in cleaned if c.strip()]
    seen = set()
    result = []
    for c in cleaned:
        key = c.lower()
        if key not in seen:
            seen.add(key)
            result.append(c)

    return result


def final_clean_language_list(langs: list[str]) -> list[str]:
    """
    Utólagos tisztítás egy játék nyelvlistáján:
    - HTML/BBCode/technikai morzsák eltávolítása
    - Tipikus kettős elemek összevonása (Simplified/Traditional Chinese,
      Spanish – Spain/LatAm, Portuguese – Brazil/Portugal)
    - Duplikátumok kiszűrése
    - LAZÁBB validáció (engedjük a kötőjelet, pontot, vesszőt,
      számot is; 2+ karakter)
    - Csak a nyilvánvaló szemét (lt, gt, br, strong, audio, support,
      text, /br) kiszűrése
    """

    if not langs or not isinstance(langs, list):
        return []

    cleaned = []
    for name in langs:
        if not name or not isinstance(name, str):
            continue
        n = html.unescape(name)
        n = re.sub(r"<[^>]*>", " ", n)
        n = re.sub(r"&lt;?/?\w+&gt;?", " ", n)
        n = re.sub(r"&[a-z]+;", " ", n)
        n = re.sub(r"[\(\)]", " ", n)
        n = re.sub(r"#lang[_\-]?", " ", n, flags=re.IGNORECASE)
        n = re.sub(r"\[/?[^\]]+\]", " ", n)

        n = re.sub(r"\b(?:lt|gt|strong|br|/br)\b", " ", n, flags=re.IGNORECASE)

        n = re.sub(r"\s+", " ", n).strip()
        if not n:
            continue

        if n.isupper():
            n = n.capitalize()

        cleaned.append(n)

    joined = []
    skip = False
    for i, word in enumerate(cleaned):
        if skip:
            skip = False
            continue
        w = word.strip()
        nxt = cleaned[i + 1].strip().lower() if i < len(cleaned) - 1 else ""

        low = w.lower()
        if i < len(cleaned) - 1:
            if low == "simplified" and nxt == "chinese":
                joined.append("Simplified Chinese")
                skip = True
                continue
            if low == "traditional" and nxt == "chinese":
                joined.append("Traditional Chinese")
                skip = True
                continue
            if low == "spanish" and "spain" in nxt:
                joined.append("Spanish - Spain")
                skip = True
                continue
            if low == "spanish" and "latin" in nxt:
                joined.append("Spanish - Latin America")
                skip = True
                continue
            if low == "portuguese" and "brazil" in nxt:
                joined.append("Portuguese - Brazil")
                skip = True
                continue
            if low == "portuguese" and "portugal" in nxt:
                joined.append("Portuguese - Portugal")
                skip = True
                continue
        joined.append(w)

    standardized = []
    for lang in joined:
        s = lang
        s = s.replace("Spanish Spain", "Spanish - Spain")
        s = s.replace("Spanish Latin America", "Spanish - Latin America")
        s = s.replace("Portuguese Brazil", "Portuguese - Brazil")
        s = s.replace("Portuguese Portugal", "Portuguese - Portugal")
        s = re.sub(r"\s+", " ", s).strip()
        standardized.append(s)

    valid_lang_pattern = re.compile(r"^[A-Za-zÀ-ÿ0-9' .,\-]{2,}$")

    hard_exclude = re.compile(
        r"\b(?:lt|gt|br|strong|audio|support|text|/br)\b",
        flags=re.IGNORECASE,
    )

    corrections_map = {
        r"\bhe ew\b": "Hebrew",
        r"\bma ese\b": "Maltese",
        r"\bazil\b": "Brazil",
        r"\bfran(?:c|ç)ais\b": "Français",
    }

    fixed = []
    for lang in standardized:
        if hard_exclude.search(lang):
            continue

        s = lang
        for wrong_re, right in corrections_map.items():
            s = re.sub(wrong_re, right, s, flags=re.IGNORECASE)

        s = re.sub(r"\s+", " ", s).strip()

        if valid_lang_pattern.match(s):
            fixed.append(s)

    seen = set()
    out = []
    for x in fixed:
        k = x.lower()
        if k not in seen:
            seen.add(k)
            out.append(x)
    return out


def clean_html_entities(text: str) -> str:
    """Eltávolítja a HTML tageket és dekódolja az entitásokat
    (pl. &reg; → ®)."""
    if pd.isna(text):
        return ""
    soup = BeautifulSoup(str(text), "html.parser")
    cleaned = soup.get_text(" ", strip=True)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned
