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
       name TEXT,                                       -- [A][B][C]
       release_date DATE,                               -- [A][B][C]
       estimated_owners INT,                            -- [A][B][C]
       required_age INT,                                -- [A][B][C]
       price FLOAT,                                     -- [A][B][C]
       DLC_count INT,                                   -- [B][C]
       num_recommendations INT,                         -- [B][C]
       notes TEXT,                                      -- [B][C]
       website TEXT,                                    -- [A][B][C]
       metacritic_score INT,                            -- [B][C]
       metacritic_url TEXT,                             -- [B][C]
       num_achievements INT,                            -- [A][B][C]
       user_score INT,                                  -- [B][C]
       score_rank INT,                                  -- [B][C]
       positive INT,                                    -- [A][B][C]
       negative INT,                                    -- [A][B][C]
       average_playtime_forever INT,                    -- [A][B][C]
       average_playtime_2weeks INT,                     -- [B][C]
       median_playtime_forever INT,                     -- [A][B][C]
       median_playtime_2weeks INT,                      -- [B][C]
       peak_ccu INT,                                    -- [B][C]
       discount INT,                                    -- [B][C]
       pct_pos_total INT,                               -- [C]
       pct_pos_recent INT,                              -- [C]
       num_reviews_total INT,                           -- [C]
       num_reviews_recent INT,                          -- [C]
       reviews TEXT,                                    -- [B][C]
       english BOOLEAN                                  -- [A]
   );

   -- ================================
   -- Támogatás, leírás, követelmények
   -- ================================
   CREATE TABLE support (
       supportid INT PRIMARY KEY,                       -- [D]
       appid INT,                                       -- [A][B][C]
       support_url TEXT,                                -- [A][B][C]
       support_email TEXT,                              -- [A][B][C]
       FOREIGN KEY (appid) REFERENCES game(appid)
   );

   CREATE TABLE requirements (                          -- [A]
       reqid INT PRIMARY KEY,
       appid INT,
       os TEXT,
       type TEXT,
       requirements TEXT,
       FOREIGN KEY (appid) REFERENCES game(appid)
   );

   CREATE TABLE description (                           
       descriptionid INT PRIMARY KEY,                   -- [D]
       appid INT,                                       -- [A][B][C]
       detailed_description TEXT,                       -- [A][C]
       about_the_game TEXT,                             -- [A][B][C]
       short_description TEXT,                          -- [A][C]
       FOREIGN KEY (appid) REFERENCES game(appid)
   );

   -- ================================
   -- Média (képek, videók)
   -- ================================
   CREATE TABLE media (                                 
       mediaid INT PRIMARY KEY,                         -- [D]
       appid INT,                                       -- [A][B][C]
       header_image TEXT,                               -- [A][B][C]
       background TEXT,                                 -- [A]
       FOREIGN KEY (appid) REFERENCES game(appid)
   );

   CREATE TABLE screenshots (                           
       screenshotid INT PRIMARY KEY,                    -- [D]
       appid INT,                                       -- [A][B][C]
       screenshots_full TEXT,                           -- [A][B][C]
       screenshots_thumbs TEXT,                         -- [A]
       FOREIGN KEY (appid) REFERENCES game(appid)
   );

   CREATE TABLE movies (                                
       movieid INT PRIMARY KEY,                         -- [D]
       appid INT,                                       -- [A][B][C]
       movies_thumbnail TEXT,                           -- [A]
       movies_max TEXT,                                 -- [A][B][C]
       movies_480 TEXT,                                 -- [A]
       FOREIGN KEY (appid) REFERENCES game(appid)
   );

   -- ================================
   -- Nyelvek és audio támogatás
   -- ================================
   CREATE TABLE languages (                             
       id INT PRIMARY KEY,                              -- [D]
       name TEXT                                        -- [B][C]
   );

   CREATE TABLE game_audio_language (                         
       appid INT,                                       -- [B][C]
       languageid INT,                                  -- [D]
       PRIMARY KEY (appid, languageid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (languageid) REFERENCES languages(id)
   );

   CREATE TABLE game_subtitles (                         
       appid INT,                                       -- [B][C]
       languageid INT,                                  -- [D]
       PRIMARY KEY (appid, languageid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (languageid) REFERENCES languages(id)
   );

   -- ================================
   -- Címkék, műfajok, kategóriák
   -- ================================
   CREATE TABLE tags (                                  
       tagid INT PRIMARY KEY,                           -- [D]
       tag_name TEXT,                                   -- [A][B][C]
       weight FLOAT                                     -- [A][B][C]
   );

   CREATE TABLE game_tag (                              -- [A]
       appid INT,                                       -- [A][B][C]
       tagid INT,                                       -- [D]
       PRIMARY KEY (appid, tagid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (tagid) REFERENCES tags(tagid)
   );

   CREATE TABLE genres (                                
       genreid INT PRIMARY KEY,                         -- [D]
       genre_name TEXT                                  -- [A][B][C]
   );

   CREATE TABLE game_genre (                            
       appid INT,                                       -- [A][B][C]
       genreid INT,                                     -- [D]   
       PRIMARY KEY (appid, genreid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (genreid) REFERENCES genres(genreid)
   );

   CREATE TABLE categories (                            
       catid INT PRIMARY KEY,                           -- [D]
       name TEXT                                        -- [A][B][C]
   );

   CREATE TABLE game_category (                         
       appid INT,                                       -- [A][B][C]
       catid INT,                                       -- [D]
       PRIMARY KEY (appid, catid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (catid) REFERENCES categories(catid)
   );

   -- ================================
   -- Fejlesztők, kiadók, platformok, csomagok
   -- ================================
   CREATE TABLE developers (                            
       devid INT PRIMARY KEY,                           -- [D]
       dev_name TEXT                                    -- [A][B][C]
   );

   CREATE TABLE game_developer (                        
       appid INT,                                       -- [A][B][C]
       devid INT,                                       -- [D]
       PRIMARY KEY (appid, devid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (devid) REFERENCES developers(devid)
   );

   CREATE TABLE publishers (                            
       pubid INT PRIMARY KEY,                           -- [D]
       pub_name TEXT                                    -- [A][B][C]
   );

   CREATE TABLE game_publisher (                        
       appid INT,                                       -- [A][B][C]
       pubid INT,                                       -- [D]
       PRIMARY KEY (appid, pubid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (pubid) REFERENCES publishers(pubid)
   );

   CREATE TABLE platforms (                             
       platid INT PRIMARY KEY,                          -- [D]
       name TEXT                                        -- [A][B][C]
   );

   CREATE TABLE game_platform (                         
       appid INT,                                       -- [A][B][C]
       platid INT,                                      -- [D]
       PRIMARY KEY (appid, platid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (platid) REFERENCES platforms(platid)
   );

   CREATE TABLE packages (                              
       packid INT PRIMARY KEY,                          -- [D]
       title TEXT,                                      -- [B][C]
       description TEXT                                 -- [B][C]
   );

   CREATE TABLE sub_package (                              
       packid INT PRIMARY KEY,                          -- [D]
       sub_text TEXT,                                   -- [B][C]
       price FLOAT,                                     -- [B][C]
       PRIMARY KEY (packid, sub_text),
       FOREIGN KEY (packid) REFERENCES packages(packid)
   );

   CREATE TABLE game_package (                          
       appid INT,                                       -- [B][C]
       packid INT,                                      -- [D]
       PRIMARY KEY (appid, packid),
       FOREIGN KEY (appid) REFERENCES game(appid),
       FOREIGN KEY (packid) REFERENCES packages(packid)
   );
