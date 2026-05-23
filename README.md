# 🧹 Cleanlytics AI

AI-Powered Enterprise Data Quality & Cleaning Automation Platform

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Scikit-Learn](https://img.shields.io/badge/ML-IsolationForest-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features
- CSV upload and profiling
- Automatic backup creation
- AI datatype suggestions
- Manual datatype control
- Data quality scoring
- Data cleaning engine
- Cleaning activity logs
- Outlier detection using IQR, Z-Score, and Isolation Forest
- PDF report generation
- Multi-page Streamlit dashboard
- Modern responsive UI

## Tech Stack
- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- ReportLab
- Plotly
- SQLite-ready architecture

## Architecture
```text
Upload Dataset
    ↓
AI Schema Detection
    ↓
Data Quality Analysis
    ↓
Data Cleaning Engine
    ↓
Outlier Detection
    ↓
PDF & CSV Export
```

## Project Structure
```text
cleanlytics-ai/
├── app.py
├── pages/
├── src/
├── data/
├── reports/
├── requirements.txt
└── README.md
```

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Workflow
1. Upload dataset
2. Review data quality
3. Check AI schema suggestions
4. Clean dataset
5. Detect outliers
6. Export cleaned file and PDF report

## Resume Project Entry
**Cleanlytics AI — AI-Powered Enterprise Data Quality Platform**

- Built a multi-page Streamlit platform for intelligent data cleaning, schema inference, outlier detection, and PDF reporting.
- Developed AI-based datatype recommendation engine with confidence scoring, issue detection, and manual schema control.
- Implemented statistical and ML-based anomaly detection using IQR, Z-Score, and Isolation Forest algorithms.
- Added enterprise-grade backup recovery, cleaning audit logs, PDF exports, and responsive SaaS-style UI architecture.
- Technologies: Python, Streamlit, Pandas, NumPy, Scikit-learn, ReportLab

## Author
Mohit Shah
