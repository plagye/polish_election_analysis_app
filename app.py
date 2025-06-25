import gradio as gr
import pandas as pd
import os
import logging
from data_processing.main_data_script import gather_data
from plotting.charts import (
    plot_top7_comparison_bar,
    plot_std_dev_timeseries,
    plot_top2_share_timeseries
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

with gr.Blocks(theme=gr.themes.Soft(), title="Polish Election Analysis") as demo:
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
                btn_plot1 = gr.Button("Top 7 Comparison")
                btn_plot2 = gr.Button("Yearly Competitiveness (Std Dev)")
                btn_plot3 = gr.Button("Top 2 Candidates' Share")
                
                plot_output_display = gr.Plot(label="Selected Plot")

                gr.Markdown(
                    "--- \n"
                    "**Top 7 Comparison:** Compares vote percentages for the top 7 candidates across election years.\n\n"
                    "**Yearly Competitiveness:** Tracks the standard deviation of vote percentages among the top 7 candidates each year. A lower value indicates a more competitive field.\n\n"
                    "**Top 2 Candidates' Share:** Shows the trend of the combined vote share of the top 2 candidates."
                )
                gr.Markdown(
                    "### Conclusions:\n"
                    "(Your detailed conclusions based on the data and plots will go here. You can reference the "
                    "insights you've already developed in your notebook. For example:)\n"
                    "*   The 2025 election shows the lowest standard deviation in vote share among the top 7 candidates since 1995, indicating a highly competitive first round.\n"
                    "*   The combined vote share of the top 2 candidates in 2025 is significantly lower than the historical average, suggesting a potential shift from traditional political dualism.*"
                )

        
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