import requests
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
import zipfile
import pandas as pd
from pandas import json_normalize
import sqlite3


url = 'https://cricsheet.org/matches/'


response = requests.get(url)



soup = BeautifulSoup(response.text, 'html.parser')


odi_links = []
for link in soup.find_all('a'):
    href = link.get('href')
    if 'odis_json' in href:
        odi_links.append(href)
print(odi_links)

odi_data_list = []

if not os.path.exists('odi_json_files'):
    os.mkdir('odi_json_files')

for link in odi_links:
    odi_url = 'https://cricsheet.org' + link
    response = requests.get(odi_url)

    # Check if the response is a ZIP file
    if response.headers.get('content-type') == 'application/zip':
        zip_filename = 'odi_json_files/' + link.split('/')[-1] + '.zip'
        
        # Save the ZIP file locally
        with open(zip_filename, 'wb') as zip_file:
            zip_file.write(response.content)
        
        # Extract the contents of the ZIP file
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall('odi_json_files')

with open('/home/deep/WorkSpace/ODI-Analysis/odi_json_files/64814.json') as f:
    json_data = json.load(f)

flattened_data= json_normalize(json_data)     
# flattened_data.to_csv('output.csv', index=False)
df = pd.DataFrame(flattened_data)
print(df)




  
