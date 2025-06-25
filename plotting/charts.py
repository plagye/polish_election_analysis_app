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