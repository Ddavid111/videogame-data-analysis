#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import ast
import pandas as pd
import logging

def create_languages_table(master_df: pd.DataFrame, output_dir: str = None):
    """
    A master_df 'supported_languages' és 'full_audio_languages' oszlopaiból
    három táblát hoz létre a relációs séma szerint:

    1. languages.csv             → id | name
    2. game_subtitles.csv        → appid | languageid  (feliratok)
    3. game_audio_language.csv   → appid | languageid  (hang)
    """
    lang_name_to_id = {}
    next_lang_id = 1

    rows_languages = []
    rows_game_subtitles = []
    rows_game_audio = []

    for _, row in master_df.iterrows():
        appid = row["appid"]

        supported_raw = row.get("supported_languages", "")
        supported = []
        if pd.notna(supported_raw) and str(supported_raw).strip():
            try:
                val = ast.literal_eval(str(supported_raw))
                if isinstance(val, list):
                    supported = [v.strip() for v in val if isinstance(v, str) and v.strip()]
                elif isinstance(val, str):
                    supported = [v.strip() for v in val.split(",") if v.strip()]
            except Exception:
                supported = [v.strip() for v in str(supported_raw).split(",") if v.strip()]

        audio_raw = row.get("full_audio_languages", "")
        full_audio = []
        if pd.notna(audio_raw) and str(audio_raw).strip():
            try:
                val = ast.literal_eval(str(audio_raw))
                if isinstance(val, list):
                    full_audio = [v.strip() for v in val if isinstance(v, str) and v.strip()]
                elif isinstance(val, str):
                    full_audio = [v.strip() for v in val.split(",") if v.strip()]
            except Exception:
                full_audio = [v.strip() for v in str(audio_raw).split(",") if v.strip()]

        all_langs = set(supported + full_audio)

        for lang in all_langs:
            if lang not in lang_name_to_id:
                lang_name_to_id[lang] = next_lang_id
                rows_languages.append({"id": next_lang_id, "name": lang})
                next_lang_id += 1

            langid = lang_name_to_id[lang]

            if lang in supported:
                rows_game_subtitles.append({"appid": appid, "languageid": langid})
            if lang in full_audio:
                rows_game_audio.append({"appid": appid, "languageid": langid})

    languages_df = pd.DataFrame(rows_languages)
    game_subtitles_df = pd.DataFrame(rows_game_subtitles)
    game_audio_df = pd.DataFrame(rows_game_audio)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        languages_df.to_csv(os.path.join(output_dir, "languages.csv"), index=False, encoding="utf-8-sig")
        game_subtitles_df.to_csv(os.path.join(output_dir, "game_subtitles.csv"), index=False, encoding="utf-8-sig")
        game_audio_df.to_csv(os.path.join(output_dir, "game_audio_language.csv"), index=False, encoding="utf-8-sig")

        logging.info(f"Saved languages ({len(languages_df)}), "
                     f"game_subtitles ({len(game_subtitles_df)}), "
                     f"game_audio_language ({len(game_audio_df)}) to {output_dir}")

    return languages_df, game_subtitles_df, game_audio_df

