from data_processing.scraper import fetch_data
from data_processing.cleaner import process_table
import pandas as pd

election_sources = {
    1995: {'url': 'https://en.wikipedia.org/wiki/1995_Polish_presidential_election', 'table_index': 12},
    2000: {'url': 'https://en.wikipedia.org/wiki/2000_Polish_presidential_election', 'table_index': 2},
    2005: {'url': 'https://en.wikipedia.org/wiki/2005_Polish_presidential_election', 'table_index': 1},
    2010: {'url': 'https://en.wikipedia.org/wiki/2010_Polish_presidential_election', 'table_index': 2},
    2015: {'url': 'https://en.wikipedia.org/wiki/2015_Polish_presidential_election', 'table_index': 2},
    2020: {'url': 'https://en.wikipedia.org/wiki/2020_Polish_presidential_election', 'table_index': 1},
    2025: {'url': 'https://en.wikipedia.org/wiki/2025_Polish_presidential_election', 'table_index': 8}
}

def gather_data():

    all_processed_dfs = []

    for year, source_info in election_sources.items():
        tables_dfs = fetch_data(source_info['url'])

        raw_table = tables_dfs[source_info['table_index']]

        processed_table = process_table(raw_table, year)

        all_processed_dfs.append(processed_table)

    final_df = pd.concat(all_processed_dfs)

    return final_df


    