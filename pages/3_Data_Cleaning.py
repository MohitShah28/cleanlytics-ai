import streamlit as st
import pandas as pd
import os
from datetime import datetime

from src.ai_schema import ai_dtype_suggestion
from src.cleaning import clean_data
from src.ui import inject_custom_css, sidebar_branding, page_header, section_title, footer

st.set_page_config(
    page_title="Data Cleaning",
    page_icon="🧹",
    layout="wide"
)
inject_custom_css()
sidebar_branding()

os.makedirs("data/cleaned", exist_ok=True)
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/backups", exist_ok=True)

page_header(
    "🧹 Data Cleaning Engine",
    "Apply safe cleaning operations with audit logs and downloads."
)
st.caption("Apply controlled cleaning actions and generate client-ready cleaned outputs.")

if "df" not in st.session_state:
    st.info("Start by uploading a CSV file in the Data Profiling page.")
    st.stop()

df = st.session_state["df"]
file_name = st.session_state.get("file_name", "uploaded_dataset.csv")

st.success(f"Using dataset: {file_name}")

st.divider()
with st.container():
    st.write("## Dataset Preview")
    st.dataframe(df.head(), use_container_width=True, hide_index=True)

# -----------------------------
# AI DATA TYPE RECOMMENDATION
# -----------------------------

st.divider()
st.write("## AI Data Type Suggestions")

dtype_options = [
    "object",
    "int",
    "float",
    "datetime",
    "category",
    "bool"
]

dtype_changes = {}

dtype_report = []

for col in df.columns:
    result = ai_dtype_suggestion(
        df[col],
        col
    )

    dtype_report.append({
        "Column": col,
        "Current Type": str(df[col].dtype),
        "Suggested Type": result["suggested_type"],
        "Confidence": f"{result['confidence']}%",
        "Reason": result["reason"]
    })

st.dataframe(pd.DataFrame(dtype_report), use_container_width=True, hide_index=True)

st.divider()
st.write("## Manual Data Type Selection")

for col in df.columns:
    result = ai_dtype_suggestion(
        df[col],
        col
    )

    suggested_dtype = result["suggested_type"]

    selected_dtype = st.selectbox(
        f"{col}",
        dtype_options,
        index=dtype_options.index(
            suggested_dtype
        ),
        key=f"dtype_{col}"
    )

    dtype_changes[col] = selected_dtype

# -----------------------------
# CLEANING OPTIONS
# -----------------------------

st.divider()
st.write("## Cleaning Options")

remove_duplicates = st.checkbox(
    "Remove Duplicate Rows"
)

fill_missing = st.checkbox(
    "Fill Missing Values"
)

drop_missing = st.checkbox(
    "Drop Missing Rows"
)

standardize_columns = st.checkbox(
    "Standardize Column Names"
)

# -----------------------------
# RUN CLEANING
# -----------------------------

if st.button("Run Data Cleaning"):
    with st.spinner("Running data cleaning..."):
        now = datetime.now()
        timestamp = now.strftime("%m_%d_%Y_%H_%M_%S")
        timestamp_display = now.strftime("%m/%d/%Y %H:%M:%S")
        task_name = "data_cleaning"
        base_name = file_name.rsplit(".", 1)[0]

        raw_path = f"data/raw/{file_name}"
        backup_path = (
            f"data/backups/"
            f"{base_name}_backup_{task_name}_{timestamp}.csv"
        )

        df.to_csv(raw_path, index=False)
        df.to_csv(backup_path, index=False)

        cleaned_df, cleaning_log = clean_data(
            df=df,
            dtype_changes=dtype_changes,
            remove_duplicates=remove_duplicates,
            fill_missing=fill_missing,
            drop_missing=drop_missing,
            standardize_columns=standardize_columns
        )

        cleaned_path = (
            f"data/cleaned/"
            f"{base_name}_cleaned_{task_name}_{timestamp}.csv"
        )

        cleaned_df.to_csv(
            cleaned_path,
            index=False
        )

    before_rows = int(df.shape[0])
    after_rows = int(cleaned_df.shape[0])
    before_missing = int(df.isnull().sum().sum())
    after_missing = int(cleaned_df.isnull().sum().sum())
    before_duplicates = int(df.duplicated().sum())
    after_duplicates = int(cleaned_df.duplicated().sum())

    before_total_cells = df.shape[0] * df.shape[1]
    after_total_cells = cleaned_df.shape[0] * cleaned_df.shape[1]

    before_missing_score = 100 - ((before_missing / before_total_cells) * 100) if before_total_cells else 0
    after_missing_score = 100 - ((after_missing / after_total_cells) * 100) if after_total_cells else 0
    before_duplicate_score = 100 - ((before_duplicates / df.shape[0]) * 100) if df.shape[0] else 0
    after_duplicate_score = 100 - ((after_duplicates / cleaned_df.shape[0]) * 100) if cleaned_df.shape[0] else 0

    st.session_state["cleaning_summary"] = {
        "before_rows": before_rows,
        "after_rows": after_rows,
        "before_missing": before_missing,
        "after_missing": after_missing,
        "before_duplicates": before_duplicates,
        "after_duplicates": after_duplicates,
        "before_quality_score": round((before_missing_score + before_duplicate_score) / 2, 2),
        "after_quality_score": round((after_missing_score + after_duplicate_score) / 2, 2)
    }

    st.success(
        "Data cleaning completed successfully!"
    )
    st.toast("Data cleaning completed successfully 🚀")
    st.info(f"Backup created: {backup_path} at {timestamp_display}")

    # -----------------------------
    # BEFORE VS AFTER
    # -----------------------------

    st.divider()
    st.write("## Before vs After Comparison")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Rows",
        after_rows,
        delta=after_rows - before_rows
    )

    col2.metric(
        "Missing Values",
        after_missing,
        delta=(after_missing - before_missing)
    )

    col3.metric(
        "Duplicate Rows",
        after_duplicates,
        delta=(after_duplicates - before_duplicates)
    )

    # -----------------------------
    # CLEANED DATA
    # -----------------------------

    st.divider()
    st.write("## Cleaned Dataset Preview")

    st.dataframe(
        cleaned_df.head(),
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------
    # CLEANING LOG
    # -----------------------------

    st.divider()
    st.write("## Cleaning Activity Log")

    if cleaning_log:
        log_df = pd.DataFrame(
            cleaning_log
        )

        st.dataframe(
            log_df,
            use_container_width=True,
            hide_index=True
        )

        log_csv = log_df.to_csv(
            index=False
        )

        st.download_button(
            label="Download Cleaning Log",
            data=log_csv,
            file_name="cleaning_log.csv",
            mime="text/csv"
        )

    # -----------------------------
    # DOWNLOAD CLEANED CSV
    # -----------------------------

    cleaned_csv = cleaned_df.to_csv(
        index=False
    )

    st.download_button(
        label="Download Cleaned CSV",
        data=cleaned_csv,
        file_name=f"{base_name}_cleaned_{task_name}_{timestamp}.csv",
        mime="text/csv"
    )

    with st.expander("Advanced: Applied Cleaning Summary"):
        st.json(st.session_state.get("cleaning_summary", {}))

footer()
