# ======== IMPORTOK ========
import os
import pandas as pd
import logging

from merge.utils.io_utils import load_csv_safely
from merge.utils.clean_utils import clean_columns


# ======== SOURCE A LOADING ========
def load_source_a(a_path: str) -> pd.DataFrame:
    """
    Betölti az A forrást (Steam CSV fájlok), megtisztítja az oszlopneveket,
    és merge-eli a különböző fájlokat egy DataFrame-be.
    """
    steam = load_csv_safely(os.path.join(a_path, "steam.csv"))
    # wrap long filename to satisfy line-length checks
    description = load_csv_safely(
        os.path.join(a_path, "steam_description_data_cleaned.csv")
    )
    media = load_csv_safely(os.path.join(a_path, "steam_media_data.csv"))
    support = load_csv_safely(os.path.join(a_path, "steam_support_info.csv"))
    tags = load_csv_safely(os.path.join(a_path, "steamspy_tag_data.csv"))
    reqs = load_csv_safely(os.path.join(a_path, "steam_requirements_data.csv"))

    for df in [steam, description, media, support, tags, reqs]:
        if not df.empty:
            df = clean_columns(df)
            possible_ids = [c for c in df.columns if "appid" in c.lower()]
            if possible_ids:
                df.rename(columns={possible_ids[0]: "appid"}, inplace=True)
    # --- SteamSpy tagok átalakítása (oszlopból dict formára) ---
    if not tags.empty:
        tag_cols = [
            c
            for c in tags.columns
            if c != "appid" and tags[c].dtype in [int, float]
        ]
        if tag_cols:
            melted = tags.melt(
                id_vars=["appid"],
                value_vars=tag_cols,
                var_name="tag_name",
                value_name="weight"
            )
            melted = melted[melted["weight"] > 0]
            tags_dict = (
                melted.groupby("appid")
                .apply(
                    lambda x: {
                        t: int(w)
                        for t, w in zip(x["tag_name"], x["weight"])
                    }
                )
                .to_dict()
            )
            tags = pd.DataFrame(
                {
                    "appid": list(tags_dict.keys()),
                    "tags": list(tags_dict.values()),
                }
            )
            logging.info(
                "SteamSpy tags converted → "
                f"{len(tags)} appid with tag data"
            )
        else:
            logging.warning(
                "No numeric tag columns found in steamspy_tag_data.csv"
            )

    merged = (
        steam.merge(description, on="appid", how="left")
        .merge(media, on="appid", how="left")
        .merge(support, on="appid", how="left")
        .merge(tags, on="appid", how="left")
        .merge(reqs, on="appid", how="left")
    )
    logging.info(f"A source merged: {len(merged)} rows")
    return merged
