# Upwork Analytics Dashboard

A comprehensive data analysis and visualization dashboard for Upwork job postings, built with Python and Streamlit.

## Overview

This project analyzes 50,000 job postings from Upwork (2024 data) to uncover job trends, pricing strategies, and geographical preferences. The dashboard provides insights into the most in-demand skills across different job categories and their corresponding compensation rates.

## Features

- **Job Metrics Overview**: Display key statistics including number of jobs, average hourly rate, average fixed price, and average estimated total pay
- **Skills Analysis**: Interactive visualizations showing the top 15 most popular skills
- **Compensation Insights**: Analysis of average pay rates for different skills
- **Interactive Dashboard**: Built with Streamlit for easy exploration and filtering

## Setup Instructions

### 1. Python Environment Setup

Set up your Python environment using Poetry:

```bash
poetry install
poetry shell
```

### 2. AI Assistant Configuration (Optional)

If using Cursor IDE with the free version:
- Connect to Claude Sonnet 3.7 API for enhanced code assistance
- This will help with code generation and debugging

## Project Structure

```
upwork-analytics/
├── README.md
├── pyproject.toml
├── upwork-analytics.py
├── upwork_cleaned.csv
└── data/
    └── (original excel files)
```

## Data Analysis Prompts

### Initial Analysis Prompt
```
The excel attachment contains job postings for 2024 in Upwork. Upwork is a popular online job platform where freelancers and businesses connect. This dataset contains 50,000 job postings from Upwork, spanning various categories and countries. With this dataset and using python language, I would like you to analyze job trends, pricing strategies, and geographical preferences of Upwork users. The end goal is to create a dashboard using streamlit. I would like you to list the python packages needed to be installed using poetry. I have a pyproject.toml file in my folder of cursor. Create the python script and insert the code into upwork-analytics.py
```

### Dashboard Creation Prompt
```
With the upwork_cleaned.csv build a dashboard to Analyze the most in-demand skills across different job categories.

Create a heading metrics for Number of Jobs, Avg Hourly Rate, Avg Fixed Price, Avg Est. Total Pay
Below the heading metrics, add a horizontal bar chart by showing the top 15 job skills on the y axis and number of jobs on the x axis. Add a title to this chart as Top skills by popularity
Below the above chart, add a horizontal bar chart which shows the same top 15 job skills by average pay
```

## Running the Dashboard

1. Ensure your Python environment is activated:
   ```bash
   poetry shell
   ```

2. Run the Streamlit dashboard:
   ```bash
   streamlit run upwork-analytics.py
   ```

3. Open your browser and navigate to the provided local URL (typically `http://localhost:8501`)

## Key Insights

The dashboard will help you discover:
- Most in-demand skills in the freelance market
- Compensation trends across different skill categories
- Market opportunities for freelancers and businesses
- Geographic distribution of job opportunities

## Data Source

- **Dataset**: 50,000 Upwork job postings from 2024
- **Coverage**: Various job categories and countries
- **Format**: Excel/CSV files with comprehensive job posting details

## Technologies Used

- **Python**: Core programming language
- **Streamlit**: Dashboard framework
- **Pandas**: Data manipulation and analysis
- **Plotly/Matplotlib**: Data visualization
- **Poetry**: Dependency management

## Contributing

Feel free to fork this repository and submit pull requests for improvements or additional features.

## License

This project is open source and available under the MIT License.
