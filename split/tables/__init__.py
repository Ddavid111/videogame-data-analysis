"""
Táblageneráló modulok a split folyamathoz.

Minden modul egy-egy tematikus CSV-t generál a merged_master adatokból:
- media_tables: képek, videók
- support_tables: support adatok
- requirements_tables: rendszerkövetelmények
- platforms_tables: operációs rendszerek
- package_tables: csomagok és alcsomagok
- developer_publisher_tables: fejlesztők és kiadók
- genre_category_tables: műfajok, kategóriák
- tags_tables: címkék (tags)
- game_metadata: leírások, alapadatok
- language_tables: támogatott nyelvek
"""

__all__ = [
    "media_tables",
    "support_tables",
    "requirements_tables",
    "platforms_tables",
    "package_tables",
    "developer_publisher_tables",
    "genre_category_tables",
    "tags_tables",
    "game_metadata",
    "language_tables",
]
