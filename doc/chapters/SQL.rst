SQL séma – D adatmodell
========================

Az alábbi SQL kód a végső D adatmodellt definiálja, amely az A, B és C
adatmodelljeinek egyesítésével készült.  
A kommentek (`-- [A]`, `-- [B]`, `-- [C]`) jelölik, hogy az adott mező vagy tábla melyik forrásból származik.

.. code-block:: sql

   -- ================================
   -- Központi tábla: game
   -- ================================
   CREATE TABLE game (
       appid INT PRIMARY KEY,                           -- [A][B][C]
       name TEXT,                                       -- [A]
       release_date TEXT,                               -- [A]
       estimated_owners TEXT,                           -- [C]
       required_age INT,                                -- [A]
       price FLOAT,                                     -- [A]
       DLC_count INT,                                   -- [A]
       recommendations INT,                             -- [A]
       notes INT,                                       -- [B]
       website TEXT,                                    -- [A]
       metacritic_score INT,                            -- [A]
       metacritic_url TEXT,                             -- [A]
       achievements INT,                                -- [A]
       user_score INT,                                  -- [B]
       score_rank int                                   -- [B]
       positive INT,                                    -- [C]
       negative INT,                                    -- [C]
       average_playtime_forever INT,                    -- [C]
       average_playtime_two_weeks INT,                  -- [C]
       median_playtime_forever INT,                     -- [C]
       median_playtime_two_weeks INT,                   -- [C]
       peak_ccu INT,                                    -- [C]
       pct_pos_total INT,                               -- [C]
       pct_pos_recent INT,                              -- [C]
       num_reviews_total INT,                           -- [C]
       num_reviews_recent INT,                          -- [C]
       reviews TEXT,                                    -- [C]
       owners TEXT,                                     -- [C]
       discount INT                                     -- [C]
   );

   -- ================================
   -- Támogatás, leírás, követelmények
   -- ================================
   CREATE TABLE support (
       supportid INT PRIMARY KEY,                       -- [A]
       appid INT,                                       -- [A]
       support_url TEXT,                                -- [A]
       support_email TEXT,                              -- [A]
       FOREIGN KEY (appid) REFERENCES game(appid)
   );

   CREATE TABLE requirements (                          -- [A]
       reqid INT PRIMARY KEY,
       appid INT,
       os TEXT,
       type TEXT,
       description TEXT,
       FOREIGN KEY (appid) REFERENCES game(appid)
   );

   CREATE TABLE description (                           -- [A]
       descriptionid INT PRIMARY KEY,
       appid INT,
       detailed_description TEXT,
       about_the_game TEXT,
       short_description TEXT,
       FOREIGN KEY (appid) REFERENCES game(appid)
   );

   -- ================================
   -- Média (képek, videók)
   -- ================================
   CREATE TABLE media (                                 -- [A]
       mediaid INT PRIMARY KEY,
       appid INT,
       header_image TEXT,
       FOREIGN KEY (appid) REFERENCES game(appid)
   );

   CREATE TABLE screenshots (                           -- [A]
       screenshotid INT PRIMARY KEY,
       appid INT,
       url TEXT,
       FOREIGN KEY (appid) REFERENCES game(appid)
   );

   CREATE TABLE movies (                                -- [A]
       movieid INT PRIMARY KEY,
       appid INT,
       url TEXT,
       FOREIGN KEY (appid) REFERENCES game(appid)
   );

   -- ================================
   -- Nyelvek és audio támogatás
   -- ================================
   CREATE TABLE languages (                             -- [B]
       langid INT PRIMARY KEY,
       lang_name TEXT
   );

   CREATE TABLE game_language (                         -- [B]
       appid INT,
       langid INT,
       audio_bool BOOLEAN,
       PRIMARY KEY (appid, langid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (langid) REFERENCES languages(langid)
   );

   -- ================================
   -- Címkék, műfajok, kategóriák
   -- ================================
   CREATE TABLE tags (                                  -- [A]
       tagid INT PRIMARY KEY,
       tag_name TEXT
   );

   CREATE TABLE game_tag (                              -- [A]
       appid INT,
       tagid INT,
       weight FLOAT,
       PRIMARY KEY (appid, tagid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (tagid) REFERENCES tags(tagid)
   );

   CREATE TABLE genres (                                -- [A]
       genreid INT PRIMARY KEY,
       genre_name TEXT
   );

   CREATE TABLE game_genre (                            -- [A]
       appid INT,
       genreid INT,
       PRIMARY KEY (appid, genreid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (genreid) REFERENCES genres(genreid)
   );

   CREATE TABLE categories (                            -- [A]
       catid INT PRIMARY KEY,
       category_name TEXT
   );

   CREATE TABLE game_category (                         -- [A]
       appid INT,
       catid INT,
       PRIMARY KEY (appid, catid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (catid) REFERENCES categories(catid)
   );

   -- ================================
   -- Fejlesztők, kiadók, platformok, csomagok
   -- ================================
   CREATE TABLE developers (                            -- [A]
       devid INT PRIMARY KEY,
       dev_name TEXT
   );

   CREATE TABLE game_developer (                        -- [A]
       appid INT,
       devid INT,
       PRIMARY KEY (appid, devid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (devid) REFERENCES developers(devid)
   );

   CREATE TABLE publishers (                            -- [A]
       pubid INT PRIMARY KEY,
       pub_name TEXT
   );

   CREATE TABLE game_publisher (                        -- [A]
       appid INT,
       pubid INT,
       PRIMARY KEY (appid, pubid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (pubid) REFERENCES publishers(pubid)
   );

   CREATE TABLE platforms (                             -- [A]
       platid INT PRIMARY KEY,
       plat_name TEXT
   );

   CREATE TABLE game_platform (                         -- [A]
       appid INT,
       platid INT,
       PRIMARY KEY (appid, platid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (platid) REFERENCES platforms(platid)
   );

   CREATE TABLE packages (                              -- [A]
       packid INT PRIMARY KEY,
       pack_name TEXT
   );

   CREATE TABLE game_package (                          -- [A]
       appid INT,
       packid INT,
       PRIMARY KEY (appid, packid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (packid) REFERENCES packages(packid)
   );
