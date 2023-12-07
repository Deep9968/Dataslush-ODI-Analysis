# To run the ODI-Analysis project, follow these steps:

1. Set up the virtual environment:
    ```
    python -m venv venv
    source venv/bin/activate
    ```

2. Install the required Python packages:
    ```
    pip install -r requirements.txt
    ```

3. Run the main.py script to extract the data from the ODI JSON files and save it to the result-data:
    ```
    python main.py
    ```


## Docker steps

1. Pull the latest MySQL image:
    ```
    docker pull mysql:latest
    ```

2. Start a MySQL container and name it mysql-odi:
    ```
    docker run -d --name mysql-odi -e MYSQL_ROOT_PASSWORD=admin -p 3306:3306 mysql:latest
    ```

3. Connect to the MySQL container as the root user:
    ```
    docker exec -it mysql-odi mysql -uroot -padmin
    ```

4. Copy the master CSV files to the MySQL container:
    ```
    docker cp result-data/master_meta.csv  mysql-odi:/var/lib/mysql-files/master_meta.csv
    docker cp result-data/master_inngings.csv  mysql-odi:/var/lib/mysql-files/master_inngings.csv
    ```


## MYSQL steps

1. Create database 
    ```
    CREATE DATABASE mydatabase;
    USE mydatabase;
    ```

2. Create cricket_innings table 
    ```
    CREATE TABLE IF NOT EXISTS cricket_innings (
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
    ```

3. Create cricket_meta table 
    ```
    CREATE TABLE IF NOT EXISTS cricket_meta (
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
    ```

4. Load the master CSV files into the tables:
    ```
    LOAD DATA LOCAL INFILE '/var/lib/mysql-files/master_meta.csv'
    INTO TABLE cricket_meta
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES;

    LOAD DATA LOCAL INFILE '/var/lib/mysql-files/master_inngings.csv'
    INTO TABLE cricket_innings
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES;
    ```


