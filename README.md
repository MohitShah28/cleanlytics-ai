# Cleanlytics AI

AI-powered enterprise data quality and cleaning automation platform.

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

## Author
Mohit Shah
