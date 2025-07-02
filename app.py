import gradio as gr
import pandas as pd
import os
import logging
from data_processing.main_data_script import gather_data
from plotting.charts import (
    plot_top7_comparison_bar,
    plot_std_dev_timeseries,
    plot_top2_share_timeseries,
    election_stats_summary
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("election_app.log"),
        logging.StreamHandler()
    ]
)

logging.info("Starting data gathering process.")
election_data = gather_data()
election_data.to_csv('election_results.csv')
logging.info("Data gathering completed.")

data = 'election_results.csv'

try:
    final_election_df = pd.read_csv(data)
    logging.info(f"Loaded data from {data}. Shape: {final_election_df.shape}")
    final_election_df = final_election_df.set_index(['Year', 'Candidate Rank'])
except Exception as e:
    logging.error(f"Error loading or processing {data}: {e}")
    raise

def gradio_plot_top7():
    logging.info("Generating Top 7 Comparison Bar plot.")
    return plot_top7_comparison_bar(final_election_df)

def gradio_plot_std_dev():
    logging.info("Generating Std Dev Timeseries plot.")
    return plot_std_dev_timeseries(final_election_df)

def gradio_plot_top2_share():
    logging.info("Generating Top 2 Share Timeseries plot.")
    return plot_top2_share_timeseries(final_election_df)

def gradio_display_dataframe():
    logging.info("Displaying DataFrame in Gradio.")
    return final_election_df.reset_index()

def gradio_stats_summary():
    return election_stats_summary(final_election_df)

conclusions_md = """
### Conclusions

**Rank 1 Candidate's result in the First Round in the 2025 Election is the lowest among Rank 1 results since 1995.**  
It is lower than the mean and its Z-score is 1.30, which indicates unusualness.

**On top of that, above I have listed Rank 2 results from years when it was higher than the result of Rank 1 Candidate in 2025.**  
This is significant because it also supports my thesis that I will state specifically after presenting one more interesting observation.

**The above numbers indicate that the First Round of 2025 Presidential Elections in Poland was indeed the most competitive first round compared to previous years (1995-2020).**  
The mean of Standard Deviations being 16.28% and the minimum being 14.22% is a staggering difference compared to 11.10%. It's an unprecedented change.  
The Z-score of negative 3.01 proves strong unusualness of the situation.  
These statistics go to show that the nation of Poland is tired of the political dualism that has been going on in the country for the past 20 years.

---
**Plot 1:**  
The bar plot above shows the first-round vote percentages for the top 7 candidates in each election year (1995–2025). This visualization allows you to compare how the distribution of votes among leading candidates has changed over time.

**Plot 2:**  
The above plot illustrates the drop in the standard deviation in 2025. It proves that the First Round of 2025 was the most competitive compared to previous years (1995-2020).

**Plot 3:**  
The above plot shows how significant was the drop of the combined vote share of the Top 2 Candidates in 2025 compared to previous years (1995-2020).  
It's another argument proving my thesis that Poles are generally drifting away from the dualism and the domination of two major parties towards something else. And I like that.
"""

with gr.Blocks(theme=gr.themes.Soft(), title="Polish Election Analysis") as demo:
    gr.HTML(
        """
        <style>
        #main-plot {
            min-height: 700px !important;
            width: 100% !important;
        }
        </style>
        """
    )
    gr.Markdown("# Polish Presidential Election: Historical First Round Analysis")
    gr.Markdown(
        "This application visualizes first-round presidential election results in Poland (1995-2025), "
        "focusing on the top 7 candidates. Data is sourced from Wikipedia."
    )

    with gr.Tabs():
        with gr.TabItem("Aggregated Data Table"):
            gr.Markdown("## Historical Election Data (Top 7 Candidates per Year)")
            gr.DataFrame(value=gradio_display_dataframe, wrap=True)
            
        with gr.TabItem("Visualizations & Analysis"):
            gr.Markdown("## Election Result Visualizations")
            with gr.Row():
                with gr.Column(scale=3):
                    btn_plot1 = gr.Button("Top 7 Comparison")
                    btn_plot2 = gr.Button("Yearly Competitiveness (Std Dev)")
                    btn_plot3 = gr.Button("Top 2 Candidates' Share")
                    # Make the plot bigger by using elem_id and CSS above
                    plot_output_display = gr.Plot(label="Selected Plot", elem_id="main-plot")
                with gr.Column(scale=2):
                    gr.Markdown("### Key Statistics")
                    stats_box = gr.Markdown(gradio_stats_summary())
                    gr.Markdown(conclusions_md)

            # Button logic
            btn_plot1.click(gradio_plot_top7, inputs=None, outputs=plot_output_display)
            btn_plot2.click(gradio_plot_std_dev, inputs=None, outputs=plot_output_display)
            btn_plot3.click(gradio_plot_top2_share, inputs=None, outputs=plot_output_display)

try:
    os.remove(data)
    logging.info(f"Temporary data file {data} removed.")
except Exception as e:
    logging.warning(f"Could not remove {data}: {e}")

if __name__ == "__main__":
    logging.info("Launching Gradio app.")
    demo.launch(server_name="0.0.0.0", server_port=7860, debug=True)