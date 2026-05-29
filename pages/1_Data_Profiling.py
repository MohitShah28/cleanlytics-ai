import streamlit as st
import pandas as pd
import os
from datetime import datetime
from src.data_formatting import read_csv_with_auto_format
from src.ui import inject_custom_css, sidebar_branding, page_header, section_title, footer

st.set_page_config(page_title="Data Profiling", page_icon="📊", layout="wide")
inject_custom_css()
sidebar_branding()

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/backups", exist_ok=True)

page_header(
    "📊 Data Profiling",
    "Upload, preview, and evaluate dataset quality."
)
st.caption("Upload once here. Other modules will use the same session dataset.")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df, format_report = read_csv_with_auto_format(uploaded_file)
    except Exception as exc:
        st.error("Unable to read this CSV file.")
        st.exception(exc)
        st.stop()

    st.session_state["df"] = df
    st.session_state["file_name"] = uploaded_file.name
    st.session_state["format_report"] = format_report

    now = datetime.now()
    timestamp_file = now.strftime("%m_%d_%Y_%H_%M_%S")
    timestamp_display = now.strftime("%m/%d/%Y %H:%M:%S")

    raw_path = f"data/raw/{uploaded_file.name}"
    backup_path = f"data/backups/backup_{timestamp_file}_{uploaded_file.name}"

    df.to_csv(raw_path, index=False)
    df.to_csv(backup_path, index=False)

    st.success("File uploaded and saved successfully!")
    if format_report.was_reformatted:
        st.warning(format_report.message)
    else:
        st.info(format_report.message)
    st.info(f"Backup created: {backup_path} at {timestamp_display}")

elif "df" in st.session_state:
    df = st.session_state["df"]
    st.success(f"Using uploaded file: {st.session_state['file_name']}")
    format_report = st.session_state.get("format_report")
    if format_report is not None:
        if format_report.was_reformatted:
            st.warning(format_report.message)
        else:
            st.info(format_report.message)

else:
    st.warning("Please upload a CSV file to start.")
    st.stop()

st.divider()
with st.container():
    st.write("## Formatted Dataset Preview")
    st.dataframe(df.head(), width="stretch")

st.divider()
with st.container():
    st.write("## Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", f"{df.shape[0]:,}")
    col2.metric("Columns", f"{df.shape[1]:,}")
    col3.metric("Missing Values", f"{int(df.isnull().sum().sum()):,}")
    col4.metric("Duplicate Rows", f"{int(df.duplicated().sum()):,}")

total_cells = df.shape[0] * df.shape[1]
missing_values = df.isnull().sum().sum()
duplicate_rows = df.duplicated().sum()

missing_score = 100 - ((missing_values / total_cells) * 100)
duplicate_score = 100 - ((duplicate_rows / df.shape[0]) * 100)

quality_score = round((missing_score + duplicate_score) / 2, 2)

st.divider()
with st.container():
    st.write("## Data Quality Score")
    st.metric("Overall Data Quality Score", f"{quality_score}/100")

if quality_score >= 90:
    st.success("Excellent data quality")
elif quality_score >= 70:
    st.warning("Moderate data quality")
else:
    st.error("Poor data quality")

st.divider()
with st.container():
    st.write("## Column Data Types")
    st.dataframe(df.dtypes.astype(str), width="stretch")

with st.expander("Advanced Dataset Details"):
    st.write("Data Type Counts")
    st.dataframe(df.dtypes.astype(str).value_counts().rename_axis("dtype").reset_index(name="count"), width="stretch")

footer()
