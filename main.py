import requests
from bs4 import BeautifulSoup
import os
import zipfile
import process


def extract():

    url = 'https://cricsheet.org/matches/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')


    odi_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if 'odis_json' in href:
            odi_links.append(href)
    

    odi_data_list = []
    if not os.path.exists('odi_json_files'):
        os.mkdir('odi_json_files')

    print('Downloading the JSON files')
    
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

    return 'successfully download the data and saved it'

if __name__ == "__main__":
    extract()
    if not os.path.exists('meta_info'):
        os.mkdir('meta_info')
    if not os.path.exists('innings'):
        os.mkdir('innings')
    if not os.path.exists('result-data'):        os.mkdir('result-data')
    process.main1()
    




  
