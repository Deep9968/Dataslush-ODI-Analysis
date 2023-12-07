CREATE TABLE IF NOT EXISTS mydatabase.cricket_innings (
    batter VARCHAR(255) NULL,
    match_id VARCHAR(255) NULL,
    non_striker VARCHAR(255) NULL,
    runs_extras VARCHAR(255) NULL,
    runs_total VARCHAR(255) NULL,
    runs_batter VARCHAR(255) NULL,
    extras_legbyes VARCHAR(255) NULL,
    `over` VARCHAR(255) NULL,
    bowler VARCHAR(255) NULL,
    team VARCHAR(255) NULL,
    ball_cnt VARCHAR(255) NULL,
    wickets_player_out VARCHAR(255) NULL,
    wickets_kind VARCHAR(255) NULL,
    wickets_fielders_name VARCHAR(255) NULL
);

LOAD DATA INFILE '/var/lib/mysql-files/master_innings.csv'
INTO TABLE mydatabase.cricket_innings
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;


CREATE TABLE IF NOT EXISTS mydatabase.cricket_meta (
    info_player_of_match_1 VARCHAR(255) NULL,
    info_team_type VARCHAR(255) NULL,
    info_event_sub_name VARCHAR(255) NULL,
    info_venue VARCHAR(255) NULL,
    match_id VARCHAR(255) NULL,
    info_toss_winner VARCHAR(255) NULL,
    info_match_type_number VARCHAR(255) NULL,
    info_outcome_method VARCHAR(255) NULL,
    registry_people VARCHAR(255) NULL,
    info_officials_match_referees VARCHAR(255) NULL,
    info_players VARCHAR(255) NULL,
    info_outcome_result VARCHAR(255) NULL,
    info_officials_reserve_umpires2 VARCHAR(255) NULL,
    info_city VARCHAR(255) NULL,
    info_player_of_match VARCHAR(255) NULL,
    info_event_stage VARCHAR(255) NULL,
    meta_created VARCHAR(255) NULL,
    registry_people_val VARCHAR(255) NULL,
    info_balls_per_over VARCHAR(255) NULL,
    supersubs_player VARCHAR(255) NULL,
    info_gender VARCHAR(255) NULL,
    meta_revision VARCHAR(255) NULL,
    missing_powerplays_category VARCHAR(255) NULL,
    info_teams VARCHAR(255) NULL,
    meta_data_version VARCHAR(255) NULL,
    target_overs VARCHAR(500) NULL,
    missing_powerplays_cnt VARCHAR(255) NULL,
    info_dates VARCHAR(255) NULL,
    supersubs_team VARCHAR(255) NULL,
    info_officials_reserve_umpires1 VARCHAR(255) NULL,
    info_season VARCHAR(255) NULL,
    info_match_type VARCHAR(255) NULL,
    info_outcome_bywickets VARCHAR(255) NULL,
    info_overs VARCHAR(255) NULL,
    info_event_group VARCHAR(255) NULL,
    info_toss_decision VARCHAR(255) NULL,
    info_event_name VARCHAR(255) NULL,
    info_player_of_match_2 VARCHAR(255) NULL,
    info_officials_umpires2 VARCHAR(255) NULL,
    info_officials_umpires1 VARCHAR(255) NULL,
    info_officials_tv_umpires VARCHAR(255) NULL,
    info_outcome_winner VARCHAR(255) NULL,
    info_event_match_number VARCHAR(255) NULL,
    info_outcome_byruns VARCHAR(255) NULL,
    target_runs VARCHAR(255) NULL,
    info_officials_reserve_umpires VARCHAR(255) NULL,
    info_outcome_eliminator VARCHAR(255) NULL
);


LOAD DATA INFILE '/var/lib/mysql-files/master_meta.csv'
INTO TABLE mydatabase.cricket_meta
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

Question 2 
----------------------------------------------------------------------------------------------
a. percentage win and total wins

WITH
  winners AS (
  SELECT
    info_outcome_winner AS info_teams,
    SUBSTRING(info_season, 1, 4) AS info_season,
    info_gender,
    COUNT(DISTINCT match_id) AS win_cnt
  FROM
    mydatabase.cricket_meta
     where info_outcome_result = 'NA'
  GROUP BY 1, 2,  3
)
SELECT
  info_teams,
  info_season,
  info_gender,
  total_cnt,
  win_cnt,
  ROUND((win_cnt / total_cnt) * 100, 2) AS percentage_win
FROM (
  SELECT
    info_teams,
    SUBSTRING(info_season, 1, 4) AS info_season,
    info_gender,
    COUNT(DISTINCT match_id) AS total_cnt
  FROM
    mydatabase.cricket_meta
  where info_outcome_result = 'NA'
  GROUP BY    1,2,3 ) AS t1
INNER JOIN
  winners
USING
  (info_teams,
    info_season,
    info_gender);

----------------------------------------------------------------------------------------------
 b. highest win percentages in 2019
WITH
  winners AS (
  SELECT
    info_outcome_winner AS info_teams,
    SUBSTRING(info_season, 1, 4) AS info_season,
    info_gender,
    COUNT(DISTINCT match_id) AS win_cnt
  FROM
    mydatabase.cricket_meta
     where info_outcome_result = 'NA'
  GROUP BY 1, 2,  3
),
raw as (

SELECT
  info_teams,
  info_season,
  info_gender,
  total_cnt,
  win_cnt,
  ROUND((win_cnt /  highest win percentages in 2019total_cnt) * 100, 2) AS percentage_win
FROM (
  SELECT
    info_teams,
    SUBSTRING(info_season, 1, 4) AS info_season,
    info_gender,
    COUNT(DISTINCT match_id) AS total_cnt
  FROM
    mydatabase.cricket_meta
  where info_outcome_result = 'NA'
  GROUP BY    1,2,3 ) AS t1
INNER JOIN
  winners
USING
  (info_teams,
    info_season,
    info_gender)
where info_season= '2019'
)

SELECT * 
FROM raw 
WHERE CONCAT(info_gender, percentage_win) IN (
    SELECT CONCAT(info_gender, max_win) 
    FROM (
        SELECT info_gender, MAX(percentage_win) AS max_win 
        FROM raw 
        GROUP BY 1
    ) t
);



