
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

OUTPUT 
+-------------+-------------+-------------+-----------+---------+----------------+
| info_teams  | info_season | info_gender | total_cnt | win_cnt | percentage_win |
+-------------+-------------+-------------+-----------+---------+----------------+
| Australia   | 2019        | female      |         8 |       8 |         100.00 |
| Netherlands | 2019        | male        |         2 |       2 |         100.00 |
+-------------+-------------+-------------+-----------+---------+----------------+

---------------------------------------------------------------------------------------------
c. Which players had the highest strike rate as batsmen in 2019?
SELECT
    batter,
    ROUND((SUM(runs_total1) / SUM(ball_cnt)) * 100, 2) AS strike
FROM (
    SELECT
        batter,
        match_id,
        SUM(runs_total) AS runs_total1,
        COUNT(runs_total) AS ball_cnt
    FROM
        mydatabase.cricket_innings
    GROUP BY 1, 2
) AS innings
INNER JOIN (
    SELECT
        SUBSTRING(info_season, 1, 4) AS info_season,
        match_id
    FROM  mydatabase.cricket_meta
    WHERE SUBSTRING(info_season, 1, 4) = '2019'
) AS metadata
USING (match_id)
GROUP BY 1
ORDER BY strike DESC
LIMIT 1;


OUTPUT:
+----------+--------+
| batter   | strike |
+----------+--------+
| KS Airee | 166.67 |
+----------+--------+
