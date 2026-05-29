# Cleanlytics AI

AI-powered enterprise data quality and cleaning automation platform built with Streamlit.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Scikit-Learn](https://img.shields.io/badge/ML-IsolationForest-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features
- CSV upload and data profiling
- Automatic CSV format detection for comma, semicolon, tab, pipe, and whitespace-separated files
- Formatted dataset preview after upload
- Automatic backup creation
- AI datatype suggestions with confidence and reasoning
- Manual datatype control
- Data quality scoring
- Data cleaning engine
- Cleaning activity logs
- Outlier detection using IQR, Z-Score, and Isolation Forest
- PDF report generation
- Multi-page Streamlit dashboard
- Portfolio screenshots in `screenshots/portfolio`

## Sample Dataset
This project includes a ready-to-use sample file:

```text
portfolio_demo_dataset.csv
```

Use this file to test the full workflow without creating your own dataset. It includes realistic customer data with missing values, duplicate rows, datatype variety, and outlier-friendly numeric values.

The app also supports messy CSV-style files where data may appear in one packed column because the separator is not a comma. During upload, Cleanlytics AI automatically detects the separator and shows a formatted preview.

## Tech Stack
- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- ReportLab
- Plotly
- SQLite-ready architecture

## Project Structure
```text
cleanlytics-ai/
|-- app.py
|-- pages/
|-- src/
|   |-- ai_schema.py
|   |-- cleaning.py
|   |-- data_formatting.py
|   |-- outliers.py
|   |-- pdf_report.py
|   `-- ui.py
|-- reports/
|-- screenshots/
|   `-- portfolio/
|-- portfolio_demo_dataset.csv
|-- requirements.txt
`-- README.md
```

## How to Run
Install dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
streamlit run app.py
```

Open the local Streamlit URL shown in your terminal, usually:

```text
http://localhost:8501
```

## Sample Workflow
1. Open the app with `streamlit run app.py`.
2. Go to `Data Profiling` from the sidebar.
3. Upload `portfolio_demo_dataset.csv`.
4. Review the `Formatted Dataset Preview`, dataset metrics, missing values, duplicates, and quality score.
5. Open `AI Schema Report` to review datatype recommendations.
6. Open `Data Cleaning`, choose cleaning options, and run the cleaning engine.
7. Open `Outlier Detection`, choose a detection method, and detect anomalies.
8. Open `Reports Export` to download cleaned CSV files, backups, and PDF reports.

## Data Formatting Behavior
When a CSV upload is not properly separated, the app tries multiple parsing strategies automatically:

- comma-separated
- semicolon-separated
- tab-separated
- pipe-separated
- whitespace-separated
- pandas auto-detected separator

If the original upload appears as one packed column, the app selects the best structured parse and displays the formatted dataframe preview before the rest of the workflow runs.

## Resume Project Entry
**Cleanlytics AI - AI-Powered Enterprise Data Quality Platform**

- Built a multi-page Streamlit platform for intelligent data cleaning, schema inference, outlier detection, and PDF reporting.
- Added automatic CSV format detection to repair messy uploads and show a structured preview.
- Developed AI-based datatype recommendation engine with confidence scoring, issue detection, and manual schema control.
- Implemented statistical and ML-based anomaly detection using IQR, Z-Score, and Isolation Forest algorithms.
- Added backup recovery, cleaning audit logs, PDF exports, sample dataset support, and responsive SaaS-style UI architecture.
- Technologies: Python, Streamlit, Pandas, NumPy, Scikit-learn, ReportLab

## Author
Mohit Shah
