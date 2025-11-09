#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import pandas as pd
from bs4 import BeautifulSoup

def clean_requirements_text(text):
    if not text or pd.isna(text):
        return ""
    soup = BeautifulSoup(str(text), "html.parser")

    for br in soup.find_all("br"):
        br.replace_with(" ")

    for li in soup.find_all("li"):
        li.replace_with(f"{li.get_text()}, ")

    cleaned = soup.get_text(separator=" ").strip()

    cleaned = re.sub(r'\s+', ' ', cleaned)

    cleaned = re.sub(r',\s*$', '', cleaned)

    cleaned = re.sub(r'^[\)\("\'\s,]+', '', cleaned)

    cleaned = re.sub(r'(?i)^(minimum|recommended)[:\s-]*', '', cleaned).strip()

    return cleaned

def split_min_rec(text):
    """
    Szétválasztja a minimum és recommended részt a stringből.
    Kis-/nagybetűt normalizál, ha a minimumban benne van a recommended, szétvágja.
    """
    if not text or pd.isna(text):
        return "", ""
    text = str(text).strip()
    parts = re.split(r"(?i)Recommended[:\s]*", text, maxsplit=1)
    min_part = parts[0].strip() if parts else ""
    rec_part = parts[1].strip() if len(parts) > 1 else ""
    return min_part, rec_part

def join_urls(x) -> str:
    """
    Lista vagy string URL-eket egységes, vesszővel elválasztott stringgé alakít.

    - Ha lista, akkor elemeit összefűzi ', ' elválasztóval.
    - Ha már string, változatlanul visszaadja.
    - Egyéb esetben üres stringet ad vissza.
    """
    if isinstance(x, list):
        return ", ".join(x)
    elif isinstance(x, str):
        return x
    return ""

