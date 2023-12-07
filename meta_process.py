import pandas as pd
import os

# schema_columns= list ({'info_event_stage', 'info_officials_match_referees', 'info_officials_umpires2', 'supersubs_player', 'info_city', 'info_event_group', 'info_player_of_match_2', 'info_team_type', 'info_match_type_number', 'info_overs', 'info_player_of_match', 'info_officials_reserve_umpires1', 'info_player_of_match_1', 'meta_created', 'info_balls_per_over', 'info_season', 'info_gender', 'info_officials_reserve_umpires2', 'info_officials_umpires1', 'info_outcome_byruns', 'info_outcome_winner', 'info_outcome_method', 'info_event_sub_name', 'info_event_name', 'registry_people', 'info_outcome_eliminator', 'info_match_type', 'meta_revision', 'target_runs', 'info_outcome_bywickets', 'meta_data_version', 'registry_people_val', 'missing_powerplays_category', 'info_toss_winner', 'info_venue', 'info_dates', 'info_players', 'info_outcome_result', 'info_officials_tv_umpires', 'info_event_match_number', 'supersubs_team', 'info_toss_decision', 'info_officials_reserve_umpires', 'target_overs', 'info_teams', 'missing_powerplays_cnt', 'match_id'})

def meta_master_csv(schema_columns):
    master_data = pd.DataFrame(columns=list(schema_columns))
   
    csv_files=[]
    for file in os.listdir('./meta_info'):
            csv_files.append(file) 

    for i in csv_files:
        individual_csv_filename = f'./meta_info/{i}'
        df = pd.read_csv(individual_csv_filename)
        df.fillna('NA', inplace=True)
        master_data = pd.concat([master_data, df], ignore_index=True)

    
    master_data.to_csv('result-data/master_meta.csv', index=False)
    print('successfully saved the master meta csv')

# meta_master_csv(schema_columns)