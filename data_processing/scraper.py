import requests
from bs4 import BeautifulSoup
import pandas as pd
import io

def fetch_data(url):
    tables_dfs = []
    
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
        
    tables = soup.find_all('table', {'class': 'wikitable'})
        
    for i, table in enumerate(tables):
        try:
            df_list = pd.read_html(io.StringIO(str(table)), header=0)
            tables_dfs.append(df_list[0])
            print(f'Succesfully parsed table {i}')
        except ValueError as e:
            print(f'ValueError parsing table {i}: {e}')
        except Exception as e:
            print(f'Other error parsing table {i}: {e}')

    return tables_dfs