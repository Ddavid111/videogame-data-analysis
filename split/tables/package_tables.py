import os
import ast
import pandas as pd
import logging


def create_packages_table(master_df: pd.DataFrame, output_dir: str):
    rows_game_package = []
    rows_packages = []
    rows_sub_package = []

    packid_counter = 1

    for _, row in master_df.iterrows():
        appid = row["appid"]
        packages_raw = row.get("packages", "")

        if pd.isna(packages_raw) or not str(packages_raw).strip():
            continue

        try:
            packages_list = ast.literal_eval(packages_raw)
        except Exception:
            continue

        if not isinstance(packages_list, list):
            continue

        for pkg in packages_list:
            title = pkg.get("title", "").strip()
            description = pkg.get("description", "").strip()

            if not title:
                continue

            rows_game_package.append({
                "appid": appid,
                "packid": packid_counter
            })

            rows_packages.append({
                "packid": packid_counter,
                "title": title,
                "description": description,
            })

            subs = pkg.get("subs", [])
            for sub in subs:
                sub_text = sub.get("text", "").strip()
                price = sub.get("price", None)
                rows_sub_package.append({
                    "packid": packid_counter,
                    "sub_text": sub_text,
                    "price": price,
                })

            packid_counter += 1

    df_game_package = pd.DataFrame(rows_game_package)
    df_packages = pd.DataFrame(rows_packages)
    df_sub_package = pd.DataFrame(rows_sub_package)

    os.makedirs(output_dir, exist_ok=True)
    df_game_package.to_csv(
        os.path.join(output_dir, "game_package.csv"), index=False
    )
    df_packages.to_csv(
        os.path.join(output_dir, "packages.csv"), index=False
    )
    df_sub_package.to_csv(
        os.path.join(output_dir, "sub_package.csv"), index=False
    )

    logging.info(f"Saved game_package.csv ({len(df_game_package)} rows)")
    logging.info(f"Saved packages.csv ({len(df_packages)} rows)")
    logging.info(f"Saved sub_package.csv ({len(df_sub_package)} rows)")

    return df_game_package, df_packages, df_sub_package
