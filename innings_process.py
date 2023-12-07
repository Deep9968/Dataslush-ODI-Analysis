import pandas as pd
import os
schema_columns= list({'runs_batter', 'non_striker', 'wickets_player_out', 'ball_cnt', 'match_id', 'extras_legbyes', 'over', 'wickets_kind', 'runs_extras', 'runs_total', 'wickets_fielders_name', 'bowler', 'team', 'batter'})

def innings_master_csv(schema_columns):
    inngins_master = pd.DataFrame(columns=list(schema_columns))
    csv_inngins=[]

    for file in os.listdir('./innings'):
            csv_inngins.append(file) 

    for i in csv_inngins:
        individual_csv_filename = f'./innings/{i}'
        df = pd.read_csv(individual_csv_filename)
        
        inngins_master = pd.concat([inngins_master, df], ignore_index=True)

    inngins_master.fillna('NA', inplace=True)
    # Save master CSV with final schema
    inngins_master.to_csv('result-data/master_innings.csv', index=False)
    print('successfully saved the master innings csv')

innings_master_csv(schema_columns)
