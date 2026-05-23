import streamlit as st
import pandas as pd
import os
from pathlib import Path
from datetime import datetime
from src.pdf_report import generate_pdf_report
from src.ai_schema import ai_dtype_suggestion
from src.outliers import (
    detect_iqr_outliers,
    detect_zscore_outliers,
    detect_isolation_forest_outliers
)
from src.ui import inject_custom_css, sidebar_branding, page_header, footer

st.set_page_config(
    page_title="Reports & Export",
    page_icon="📄",
    layout="wide"
)
inject_custom_css()
sidebar_branding()

page_header(
    "📄 Reports & Export",
    "Download cleaned datasets, backups, and PDF reports."
)
st.caption("Central hub for generated files and client-facing PDF reports.")


def infer_source_section(file_name, is_backup=False):
    if "data_cleaning" in file_name:
        if is_backup or "_backup_" in file_name:
            return "3_Data_Cleaning (Backup Snapshot)"
        return "3_Data_Cleaning"
    if "data_profiling" in file_name:
        return "1_Data_Profiling"
    if "ai_schema_report" in file_name:
        return "2_AI_Schema_Report"
    if "outlier_detection" in file_name or "outlier_report" in file_name:
        return "4_Outlier_Detection"
    if "reports_export" in file_name:
        return "5_Reports_Export"
    return "Unknown / Manual"

# -----------------------------
# CLEAR EXPORT FILES
# -----------------------------

st.write("## Maintenance")

if st.button("Remove All Export Files", key="remove_all_export_files"):
    folders_to_clear = ["data/cleaned", "data/backups"]
    deleted_count = 0

    for folder in folders_to_clear:
        folder_path = Path(folder)
        if folder_path.exists():
            for file_path in folder_path.iterdir():
                if file_path.is_file():
                    file_path.unlink()
                    deleted_count += 1

    if deleted_count > 0:
        st.success(f"Removed {deleted_count} files from cleaned and backup folders.")
    else:
        st.info("No files found to remove.")

st.divider()

# -----------------------------
# CLEANED FILES
# -----------------------------

st.write("## Cleaned Dataset Files")

cleaned_folder = "data/cleaned"

if os.path.exists(cleaned_folder):

    cleaned_files = os.listdir(cleaned_folder)

    if cleaned_files:
        cleaned_info = pd.DataFrame(
            [
                {
                    "File Name": file,
                    "Source Section": infer_source_section(file)
                }
                for file in sorted(cleaned_files)
            ]
        )

        st.dataframe(cleaned_info, use_container_width=True, hide_index=True)

        for file in sorted(cleaned_files):

            file_path = os.path.join(
                cleaned_folder,
                file
            )

            with open(file_path, "rb") as f:

                st.download_button(
                    label=f"Download {file}",
                    data=f,
                    file_name=file,
                    mime="text/csv",
                    key=f"download_cleaned_{file}"
                )

    else:
        st.info("No cleaned files found.")

else:
    st.info("Cleaned data folder not found.")

st.divider()

# -----------------------------
# BACKUP FILES
# -----------------------------

st.write("## Backup Dataset Files")

backup_folder = "data/backups"

if os.path.exists(backup_folder):

    backup_files = os.listdir(backup_folder)

    if backup_files:
        backup_info = pd.DataFrame(
            [
                {
                    "File Name": file,
                    "Source Section": infer_source_section(file, is_backup=True)
                }
                for file in sorted(backup_files)
            ]
        )

        st.dataframe(backup_info, use_container_width=True, hide_index=True)

        for file in sorted(backup_files):

            file_path = os.path.join(
                backup_folder,
                file
            )

            with open(file_path, "rb") as f:

                st.download_button(
                    label=f"Download Backup: {file}",
                    data=f,
                    file_name=file,
                    mime="text/csv",
                    key=f"download_backup_{file}"
                )

    else:
        st.info("No backup files found.")

else:
    st.info("Backup folder not found.")

st.divider()

# -----------------------------
# PDF REPORT GENERATOR
# -----------------------------

st.write("## Generate PDF Report")

if "df" not in st.session_state:
    st.info("Start by uploading a CSV file in the Data Profiling page.")
else:
    df = st.session_state["df"]
    file_name = st.session_state.get(
        "file_name",
        "dataset.csv"
    )

    total_cells = df.shape[0] * df.shape[1]
    missing_values = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()

    if total_cells == 0:
        missing_score = 100
    else:
        missing_score = 100 - ((missing_values / total_cells) * 100)

    if df.shape[0] == 0:
        duplicate_score = 100
    else:
        duplicate_score = 100 - ((duplicate_rows / df.shape[0]) * 100)

    quality_score = round(
        (missing_score + duplicate_score) / 2,
        2
    )

    if st.button("Generate PDF Report", key="generate_pdf_report"):
        with st.spinner("Generating PDF report..."):
            os.makedirs("reports", exist_ok=True)
            now = datetime.now()
            timestamp = now.strftime("%m_%d_%Y_%H_%M_%S")
            timestamp_display = now.strftime("%m/%d/%Y %H:%M:%S")
            pdf_filename = f"cleanlytics_report_{timestamp}.pdf"
            pdf_path = f"reports/{pdf_filename}"

            dtype_report = []
            for col in df.columns:
                result = ai_dtype_suggestion(df[col], col)
                dtype_report.append({
                    "Column": col,
                    "Current Data Type": str(df[col].dtype),
                    "AI Suggested Type": result["suggested_type"],
                    "Confidence": f"{result['confidence']}%",
                    "Reason": result["reason"]
                })

            iqr_df = detect_iqr_outliers(df)
            zscore_df = detect_zscore_outliers(df)
            iso_df = detect_isolation_forest_outliers(df)

            generate_pdf_report(
                file_path=pdf_path,
                dataset_name=file_name,
                rows=df.shape[0],
                columns=df.shape[1],
                missing_values=missing_values,
                duplicate_rows=duplicate_rows,
                quality_score=quality_score,
                schema_rows=dtype_report,
                iqr_outliers=iqr_df.to_dict("records") if not iqr_df.empty else [],
                zscore_outliers=zscore_df.to_dict("records") if not zscore_df.empty else [],
                iso_outliers=iso_df.to_dict("records") if not iso_df.empty else [],
                cleaning_summary=st.session_state.get("cleaning_summary"),
                cleaned_file_count=len(os.listdir("data/cleaned")) if os.path.exists("data/cleaned") else 0,
                backup_file_count=len(os.listdir("data/backups")) if os.path.exists("data/backups") else 0
            )

            st.success(f"PDF report generated successfully at {timestamp_display}!")
            st.toast("PDF report generated successfully 📄")

            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_file,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    key="download_pdf_report"
                )

    with st.expander("Advanced: Report Inputs Used"):
        st.write(
            f"Dataset: `{file_name}` | Rows: `{df.shape[0]}` | Columns: `{df.shape[1]}` | "
            f"Missing: `{missing_values}` | Duplicates: `{duplicate_rows}` | Score: `{quality_score}`"
        )

footer()
