import os
import pandas as pd
import logging


def create_support_table(master_df: pd.DataFrame,
                         output_dir: str = None) -> pd.DataFrame:
    """
    Létrehozza a support táblát a merged_master-ből.
    Tartalmazza:
      - supportid (1-től generált)
      - appid
      - support_url
      - support_email
    """
    cols = ["appid"]
    for c in ["support_url", "support_email"]:
        if c in master_df.columns:
            cols.append(c)

    df = master_df[cols].copy()

    for c in ["support_url", "support_email"]:
        if c in df.columns:
            df[c] = df[c].fillna("").astype(str)

    df = df[
        (df.get("support_url", "") != "")
        | (df.get("support_email", "") != "")
    ].reset_index(drop=True)

    df.insert(0, "supportid", range(1, len(df) + 1))

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "support.csv")
        df.to_csv(path, index=False)
        logging.info(f"Saved 'support.csv' ({len(df)} rows) to {output_dir}")

    return df
