import pandas as pd

def process_table(raw_results_df, year):
    results_df = raw_results_df
    
    if year == 2000:
        selected_cols = {
            'Candidate': results_df['Candidate.1'],
            'First Round Votes': results_df['Votes'],
            'First Round %': results_df['%'],
        }
    
    else:
        new_header = results_df.iloc[0]
        results_df = results_df[1:]
        results_df.columns = new_header
        
        selected_cols = {
            'Candidate': results_df['Candidate'].iloc[:, 0],
            'First Round Votes': results_df['Votes'].iloc[:, 0],
            'First Round %': results_df['%'].iloc[:, 0],
        }
        
    results_df = pd.DataFrame(selected_cols)
    results_df['First Round Votes'] = pd.to_numeric(results_df['First Round Votes'], errors='coerce')
    results_df['First Round %'] = pd.to_numeric(results_df['First Round %'], errors='coerce')
    results_df = results_df.head(7)
    results_df = results_df.sort_values(by='First Round Votes', ascending=False).reset_index(drop=True)
    results_df['Candidate Rank'] = results_df.index + 1
    results_df = results_df.drop(columns=['Candidate'])
    results_df['Year'] = year
    results_df = results_df.set_index(['Year', 'Candidate Rank'])

    return results_df