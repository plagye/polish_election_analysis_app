import matplotlib.pyplot as plt
import pandas as pd

def plot_top7_comparison_bar(data_df):
    vote_pct_df = data_df['First Round %'].unstack(level='Candidate Rank')
    fig, ax = plt.subplots(figsize=(18, 10))
    vote_pct_df.plot(kind='bar', ax=ax)
    ax.set_title('First Round Vote Percentage for Top 7 Candidates by Year', fontsize=16)
    ax.set_ylabel('Vote Percentage (%)', fontsize=12)
    ax.set_xlabel('Election Year', fontsize=12)
    ax.tick_params(rotation=45)
    ax.legend(title='Candidate Rank', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    fig.tight_layout(rect=[0, 0, 0.85, 1])
    return fig

def plot_std_dev_timeseries(data_df):
    vote_pct_df = data_df['First Round %'].unstack(level='Candidate Rank')
    std_per_year = vote_pct_df.std(axis=1)
    mean_std = std_per_year.mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    std_per_year.plot(kind='line', marker='o', linestyle='-', color='tab:blue', ax=ax)
    ax.axhline(mean_std, color='r', linestyle='--',
               label=f'Historical Mean Std Dev ({mean_std:.2f}%)')
    ax.scatter(std_per_year.index[-1], std_per_year.iloc[-1], color='red', s=100, zorder=5, label=f'{std_per_year.index[-1]} Std Dev')
    ax.set_title('Standard Deviation of Vote Percentages Among Top 7 Candidates (Per Year)', fontsize=15)
    ax.set_ylabel('Standard Deviation of %', fontsize=12)
    ax.set_xlabel('Election Year', fontsize=12)
    ax.set_xticks(std_per_year.index.tolist())
    ax.legend()
    ax.grid(True, linestyle=':', alpha=0.7)
    fig.tight_layout()
    return fig

def plot_top2_share_timeseries(data_df):
    vote_pct_df = data_df['First Round %'].unstack(level='Candidate Rank')
    top2_df = vote_pct_df[[1, 2]].rename(columns={1: '1', 2: '2'})
    top2_df['Top 2 Share'] = top2_df['1'] + top2_df['2']
    mean_top2_share = top2_df['Top 2 Share'].mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    top2_df['Top 2 Share'].plot(kind='line', marker='o', linestyle='-', color='tab:blue', label='Top-2 Share', ax=ax)
    ax.axhline(mean_top2_share, color='r', linestyle='--',
               label=f'Mean Top-2 Share ({mean_top2_share:.2f}%)')
    ax.scatter(top2_df.index[-1], top2_df['Top 2 Share'].iloc[-1], color='red', s=100, zorder=5, label=f'{top2_df.index[-1]} Top-2')
    ax.set_title('Combined First-Round Vote Share of Top 2 Candidates by Year', fontsize=15)
    ax.set_xlabel('Election Year', fontsize=12)
    ax.set_ylabel('Combined Top-2 Share (%)', fontsize=12)
    ax.set_ylim(60, 80)
    ax.set_xticks(top2_df.index.tolist())
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend()
    fig.tight_layout()
    return fig

def election_stats_summary(final_df):
    """
    Returns a formatted string with key statistics for top 1 and 2 candidates and the spread among top 7,
    based on the structure of your Jupyter notebook code.
    """
    # Historical stats for Rank 1 (excluding 2025)
    historical_rank1 = final_df.xs(1, level='Candidate Rank')['First Round %']
    historical_rank1 = historical_rank1.drop(2025, errors='ignore')

    historical_mean_rank1 = historical_rank1.mean()
    historical_std_rank1 = historical_rank1.std()
    historical_min_rank1 = historical_rank1.min()
    historical_max_rank1 = historical_rank1.max()

    # 2025 and other years for Rank 1 and Rank 2
    perc_2025_r1 = final_df.loc[(2025, 1), 'First Round %'] if (2025, 1) in final_df.index else float('nan')
    perc_2015_r2 = final_df.loc[(2015, 2), 'First Round %'] if (2015, 2) in final_df.index else float('nan')
    perc_2010_r2 = final_df.loc[(2010, 2), 'First Round %'] if (2010, 2) in final_df.index else float('nan')
    perc_2005_r2 = final_df.loc[(2005, 2), 'First Round %'] if (2005, 2) in final_df.index else float('nan')
    perc_1995_r2 = final_df.loc[(1995, 2), 'First Round %'] if (1995, 2) in final_df.index else float('nan')

    z_score = abs((perc_2025_r1 - historical_mean_rank1) / historical_std_rank1) if not pd.isna(perc_2025_r1) else float('nan')

    # Spread among Top 7
    plot_final_df = final_df['First Round %'].unstack(level='Candidate Rank')
    historical_df = plot_final_df[plot_final_df.index != 2025]
    historical_within_year_std = historical_df.std(axis=1)

    mean_historical_within_year_std = historical_within_year_std.mean()
    std_historical_within_year_std = historical_within_year_std.std()

    if 2025 in final_df.index.get_level_values(0):
        percentages_top7_2025 = final_df.loc[2025, 'First Round %'].values
        std_dev_within_2025 = percentages_top7_2025.std()
        z_score_of_std = (std_dev_within_2025 - mean_historical_within_year_std) / std_historical_within_year_std
    else:
        std_dev_within_2025 = float('nan')
        z_score_of_std = float('nan')

    # Format output
    summary = (
        f"**Historical Mean % for Rank 1 (1995–2020):** {historical_mean_rank1:.2f}%\n"
        f"**Historical Std Dev for Rank 1 (1995–2020):** {historical_std_rank1:.2f}%\n"
        f"**Historical Min % for Rank 1 (1995–2020):** {historical_min_rank1:.2f}%\n"
        f"**Historical Max % for Rank 1 (1995–2020):** {historical_max_rank1:.2f}%\n\n"
        f"**2025 Percentage for Rank 1:** {perc_2025_r1:.2f}%\n\n"
        f"**2015 Percentage for Rank 2:** {perc_2015_r2:.2f}%\n"
        f"**2010 Percentage for Rank 2:** {perc_2010_r2:.2f}%\n"
        f"**2005 Percentage for Rank 2:** {perc_2005_r2:.2f}%\n"
        f"**1995 Percentage for Rank 2:** {perc_1995_r2:.2f}%\n\n"
        f"**Z-score for 2025 Rank 1:** {z_score:.2f}\n\n"
        f"**Mean of historical within-year Std Devs (Top 7):** {mean_historical_within_year_std:.2f}%\n"
        f"**Standard Deviation of percentages among Top 7 in 2025:** {std_dev_within_2025:.2f}%\n"
        f"**Z-score for the spread (std dev) of Top 7 in 2025:** {z_score_of_std:.2f}\n"
    )
    return summary