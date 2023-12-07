import json
from pandas import json_normalize
import sqlite3
import csv
import pandas as pd
import os 
import meta_process
import innings_process



def json_dataframe(flat_data,pep1,val1):
   
    team1 = flat_data.copy() 
    team1["registry_people"] = pep1
    team1["registry_people_val"] = val1 
    key1='info_players_'+team1["info_teams_1"]
    key2='info_players_'+team1["info_teams_2"]
    players1={ }

    if key1 in team1:
        del team1[key2]
        del team1["info_teams_2"]
        team1["info_players"] = team1.pop(key1)
        players1['info_players'] = team1["info_players"]
        del team1["info_players"] 
        team1["info_teams"] = team1.pop('info_teams_1')
        df1 = pd.DataFrame(team1)
        play1 = pd.DataFrame(players1)
        result_data1 = pd.concat([df1,play1], axis=1)

    team2 = flat_data.copy() 
    team2["registry_people"] = pep1
    team2["registry_people_val"] = val1 
    players2={ }

    if key2 in team2:
        del team2[key1]
        del team2["info_teams_1"]
        team2["info_players"] = team2.pop(key2)
        players2['info_players'] = team2["info_players"]
        del team2["info_players"] 
        team2["info_teams"] = team2.pop('info_teams_2')
        df2 = pd.DataFrame(team2)
        play2 = pd.DataFrame(players2)
        result_data2 = pd.concat([df2,play2], axis=1)
        

    result_data = pd.concat([result_data1,result_data2], ignore_index=True)
    
    return result_data




def flatten_json(data,file_name,schema_columns):
    file_name= file_name.split('.')[0]
    flat_data = {} 
    pep1=[]
    val1=[]
    for key, value in data.items():

        if isinstance(value,dict) and key != "innings": 
            for i_key,j_value in value.items():   
  

                if isinstance(j_value,list) and len(j_value)==1  and  i_key !='missing':             
                    flat_data[key+'_'+i_key]=j_value[0]    # info_dates : '2002-12-29' 
                        
                elif isinstance(j_value,list) and len(j_value)!=1  and  i_key =='dates':             
                    flat_data[key+'_'+i_key]=', '.join(j_value)  

                elif  isinstance(j_value,dict) and i_key=='supersubs' : 
                    flat_data['supersubs_team']=list(j_value.keys())[0]
                    flat_data['supersubs_player']=list(j_value.values())[0]    

                elif  isinstance(j_value,list) and i_key=='missing' :             
                    # print(i_key,j_value[0])
                    if isinstance(j_value[0],dict) :
                        for missing_key, missing_value in j_value[0].items():
                            flat_data[f'missing_{missing_key}'] = missing_value
                        flat_data['missing_powerplays_cnt']=list(flat_data['missing_powerplays'].keys())[0]
                        flat_data['missing_powerplays_category']=list(flat_data['missing_powerplays'].values())[0][0]
                        del flat_data['missing_powerplays']
                    else:
                        flat_data['missing_powerplays_category']=j_value[0]
                    
                elif isinstance(j_value,list) and len(j_value)==2 : 
                    flat_data[key+'_'+i_key+'_'+'1']=j_value[0]
                    flat_data[key+'_'+i_key+'_'+'2']=j_value[1]

                elif isinstance(j_value,dict):              # officials
                    if i_key == "registry":
                        for pep, val in j_value['people'].items():
                                 pep1.append(pep)
                                 val1.append(val)
                    else:                                
                        for i,j in j_value.items() :
                            if isinstance(j,list) and len(j)==1: 
                                 flat_data[key+'_'+i_key+'_'+i]=j[0]

                            elif isinstance(j,list) and len(j)==2: 
                                 flat_data[key+'_'+i_key+'_'+i+'1']=j[0]
                                 flat_data[key+'_'+i_key+'_'+i+'2']=j[1]

                            elif isinstance(j,dict): 
                                flat_data[key+'_'+i_key+'_'+i+list(j.keys())[0]]=list(j.values())[0]
                                 
                            else:                
                                flat_data[key+'_'+i_key+'_'+i]=j
                else:
                    flat_data[key+'_'+i_key]=j_value  
                
    
    for inning in data["innings"]:
       target1= inning.get("target")
       if target1!=None:
           for target_key, target_value in target1.items():
               flat_data['target'+'_'+target_key]=target_value   
     
    # print(json.dumps(flat_data, indent=1))

    flat_data['match_id']=file_name
    result_data = json_dataframe(flat_data, pep1, val1)
    result_data.to_csv(f'meta_info/{file_name}.csv', index=False)
    

    schema_columns.update(result_data.columns)
    return  schema_columns

    

    

# print(json.dumps(value[0]['overs'], indent=1))

def innings(data,file_name,schema_columns):
 file_name= file_name.split('.')[0]

 for inning in data["innings"]:
    for over in inning["overs"]:
        ball_cnt=1
        for delivery in over["deliveries"]:
            
            if "extras" in delivery:
                for extra_key, extra_value in delivery["extras"].items():
                    delivery[f'extras_{extra_key}'] = extra_value
                del delivery["extras"]

            
            if "runs" in delivery:
                for run_key, run_value in delivery["runs"].items():
                    delivery[f'runs_{run_key}'] = run_value
                del delivery["runs"]

            if "wickets" in delivery:
                
                for wickets_key, wickets_value in delivery['wickets'][0].items():
                    delivery[f'wickets_{wickets_key}'] = wickets_value
                del delivery["wickets"]
                # print(delivery['wickets'])

            if "wickets_fielders" in delivery:
                
                for wickets_fielders_key, wickets_fielders_value in delivery['wickets_fielders'][0].items():
                    delivery[f'wickets_fielders_{wickets_fielders_key}'] = wickets_fielders_value
                del delivery["wickets_fielders"]
            
            delivery["ball_cnt"]=ball_cnt
            ball_cnt+=1
    

    innings_data = []
    for inning in data["innings"]:
        team = inning["team"]
        for over_data in inning["overs"]:
            over = over_data["over"]
            for delivery_data in over_data["deliveries"]:
                innings_data.append(
                    {
                        "team": team,
                        "over": over,
                        "batter": delivery_data["batter"],
                        "bowler": delivery_data["bowler"],
                        "non_striker": delivery_data["non_striker"],
                        "extras_legbyes": delivery_data.get("extras_legbyes", 0),
                        "runs_batter": delivery_data.get("runs_batter", 0),
                        "runs_extras": delivery_data.get("runs_extras", 0),
                        "runs_total": delivery_data.get("runs_total", 0),
                        "wickets_player_out": delivery_data.get("wickets_player_out", 'na'),
                        "wickets_kind": delivery_data.get("wickets_kind", 'na'),
                        "wickets_fielders_name": delivery_data.get("wickets_fielders_name", 'na'),
                        "ball_cnt":delivery_data.get("ball_cnt", 'na'),
                        "match_id":file_name
                    }
                )

    
    df= pd.DataFrame(innings_data)
    df.to_csv(f'innings/{file_name}.csv', index=False)
    
    schema_columns.update(df.columns)
    return  schema_columns
    
def main1():   
        # meta_info
        json_files=[]
        for file in os.listdir('./odi_json_files'):
            if file.endswith('.json'):
                json_files.append(file) 
        
        schema_meta = set()
        schema_innings = set()

        cnt = 1
        print('Transforming the JSON data into two master CSV')
        for i in json_files:
            with open(f'./odi_json_files/{i}') as f:
                data = json.load(f)
                schema_columns1 = flatten_json(data, i, schema_meta)
                schema_columns2 = innings(data, i, schema_innings)
                cnt += 1
        meta_process.meta_master_csv(schema_columns1)
        innings_process.innings_master_csv(schema_columns2)

