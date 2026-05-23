import streamlit as st
import pandas as pd
import os
from datetime import datetime

from src.outliers import (
    detect_iqr_outliers,
    detect_zscore_outliers,
    detect_isolation_forest_outliers,
    fix_iqr_outliers,
    fix_zscore_outliers
)
from src.ui import inject_custom_css, sidebar_branding, page_header, section_title, footer

st.set_page_config(
    page_title="Outlier Detection",
    page_icon="🚨",
    layout="wide"
)
inject_custom_css()
sidebar_branding()

page_header(
    "🚨 Outlier Detection",
    "Detect abnormal numeric values using statistical and ML methods."
)
st.caption("Detect potential anomalies using statistical and ML-based methods.")

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

st.divider()
st.write("## Select Detection Method")

outlier_method = st.selectbox(
    "Choose outlier detection method",
    ["IQR", "Z-Score", "Isolation Forest"]
)

if st.button("Detect Outliers"):
    with st.spinner("Detecting outliers..."):
        if outlier_method == "IQR":
            outlier_df = detect_iqr_outliers(df)
        elif outlier_method == "Z-Score":
            outlier_df = detect_zscore_outliers(df)
        else:
            outlier_df = detect_isolation_forest_outliers(df)
    st.session_state["outlier_df"] = outlier_df
    st.session_state["outlier_method"] = outlier_method
    st.toast("Outlier detection completed 🚨")

saved_outlier_df = st.session_state.get("outlier_df")
saved_outlier_method = st.session_state.get("outlier_method", outlier_method)

if saved_outlier_df is not None:
    if not saved_outlier_df.empty:
        st.warning("Outliers detected.")
        st.dataframe(saved_outlier_df, use_container_width=True, hide_index=True)
        st.metric("Detected Outlier Entries", f"{len(saved_outlier_df):,}")

        outlier_csv = saved_outlier_df.to_csv(index=False)

        st.download_button(
            label="Download Outlier Report",
            data=outlier_csv,
            file_name="outlier_report.csv",
            mime="text/csv"
        )

        st.write("## Fix Detected Outliers")
        st.caption(f"Current detection method: `{saved_outlier_method}`")

        fix_strategy = st.selectbox(
            "Select fixing strategy",
            ["cap", "median", "remove"],
            key="fix_strategy"
        )

        if st.button("Fix Outliers", key="fix_outliers_btn"):
            with st.spinner("Fixing outliers..."):
                os.makedirs("data/backups", exist_ok=True)
                now = datetime.now()
                timestamp = now.strftime("%m_%d_%Y_%H_%M_%S")
                timestamp_display = now.strftime("%m/%d/%Y %H:%M:%S")
                backup_path = (
                    f"data/backups/"
                    f"before_outlier_fix_{timestamp}.csv"
                )
                df.to_csv(backup_path, index=False)

                before_rows = len(df)
                before_outlier_entries = len(saved_outlier_df)

                if saved_outlier_method == "IQR":
                    fixed_df, fix_log = fix_iqr_outliers(df, strategy=fix_strategy)
                    post_outlier_df = detect_iqr_outliers(fixed_df)
                elif saved_outlier_method == "Z-Score":
                    fixed_df, fix_log = fix_zscore_outliers(df, strategy=fix_strategy)
                    post_outlier_df = detect_zscore_outliers(fixed_df)
                else:
                    st.warning(
                        "Isolation Forest fixing is not enabled yet. Use it for detection first."
                    )
                    st.stop()

                st.session_state["df"] = fixed_df
                os.makedirs("data/cleaned", exist_ok=True)
                fixed_path = (
                    f"data/cleaned/"
                    f"outlier_fixed_{timestamp}.csv"
                )
                fixed_df.to_csv(fixed_path, index=False)
                st.session_state["outlier_df"] = post_outlier_df
                st.session_state["outlier_method"] = saved_outlier_method

                after_rows = len(fixed_df)
                after_outlier_entries = len(post_outlier_df)

                st.success("Outliers fixed successfully.")
                st.info(f"Backup created: {backup_path} at {timestamp_display}")
                st.success(f"Fixed dataset saved: {fixed_path} at {timestamp_display}")
                st.toast("Outlier fixing completed.")

                col1, col2 = st.columns(2)
                col1.metric("Rows After Fix", f"{after_rows:,}", delta=after_rows - before_rows)
                col2.metric(
                    "Outlier Entries After Fix",
                    f"{after_outlier_entries:,}",
                    delta=after_outlier_entries - before_outlier_entries
                )

                if not fix_log.empty:
                    st.write("### Fix Activity Log")
                    st.dataframe(fix_log, use_container_width=True, hide_index=True)
                else:
                    st.info("No outliers were changed with the selected strategy.")

                st.write("## Outlier Fix Summary")
                col1, col2 = st.columns(2)
                col1.metric(
                    "Rows After Fix",
                    fixed_df.shape[0]
                )
                total_fixed = (
                    fix_log["Outliers Fixed"].sum()
                    if "Outliers Fixed" in fix_log.columns
                    else 0
                )
                col2.metric(
                    "Total Outliers Fixed",
                    int(total_fixed)
                )

                st.write("### Before vs After Outlier Report")
                before_df = saved_outlier_df.copy()
                after_df = post_outlier_df.copy()

                if "Outliers Found" in before_df.columns:
                    before_df = before_df.rename(
                        columns={"Outliers Found": "Outliers Before"}
                    )
                if "Outliers Found" in after_df.columns:
                    after_df = after_df.rename(
                        columns={"Outliers Found": "Outliers After"}
                    )

                merge_keys = ["Column", "Method"]
                before_keep = [c for c in ["Column", "Method", "Outliers Before"] if c in before_df.columns]
                after_keep = [c for c in ["Column", "Method", "Outliers After"] if c in after_df.columns]

                # Ensure merge keys exist even when one side is empty/no-outlier result.
                for key in merge_keys:
                    if key not in before_df.columns:
                        before_df[key] = ""
                    if key not in after_df.columns:
                        after_df[key] = ""

                before_subset = before_df[[c for c in ["Column", "Method", "Outliers Before"] if c in before_df.columns]]
                after_subset = after_df[[c for c in ["Column", "Method", "Outliers After"] if c in after_df.columns]]

                if "Outliers Before" not in before_subset.columns:
                    before_subset["Outliers Before"] = 0
                if "Outliers After" not in after_subset.columns:
                    after_subset["Outliers After"] = 0

                comparison_df = before_subset.merge(
                    after_subset,
                    on=merge_keys,
                    how="outer"
                ).fillna(0)

                if "Outliers Before" in comparison_df.columns and "Outliers After" in comparison_df.columns:
                    comparison_df["Outliers Before"] = comparison_df["Outliers Before"].astype(int)
                    comparison_df["Outliers After"] = comparison_df["Outliers After"].astype(int)
                    comparison_df["Difference"] = (
                        comparison_df["Outliers After"] - comparison_df["Outliers Before"]
                    )

                st.dataframe(comparison_df, use_container_width=True, hide_index=True)

                fixed_csv = fixed_df.to_csv(index=False)
                st.download_button(
                    label="Download Outlier-Fixed Dataset",
                    data=fixed_csv,
                    file_name=f"outlier_fixed_{timestamp}.csv",
                    mime="text/csv"
                )
    else:
        st.success("No major outliers detected.")

with st.expander("Advanced: Detection Method Guidance"):
    st.write(
        "- `IQR`: strong for skewed numeric columns\n"
        "- `Z-Score`: useful when data is near-normal\n"
        "- `Isolation Forest`: model-based multi-column anomaly detection"
    )

footer()
