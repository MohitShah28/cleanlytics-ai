import streamlit as st
import pandas as pd
from src.ai_schema import ai_dtype_suggestion
from src.ui import inject_custom_css, sidebar_branding, page_header, section_title, footer

st.set_page_config(page_title="AI Schema Report", page_icon="🤖", layout="wide")
inject_custom_css()
sidebar_branding()

page_header(
    "🤖 AI Schema Report",
    "Review AI datatype suggestions with confidence and reasoning."
)
st.caption("AI-assisted column type recommendations and confidence insights.")

if "df" not in st.session_state:
    st.info("Start by uploading a CSV file in the Data Profiling page.")
    st.stop()

df = st.session_state["df"]
file_name = st.session_state.get("file_name", "uploaded_dataset.csv")

st.success(f"Using dataset: {file_name}")
st.divider()

with st.spinner("Analyzing schema with AI suggestions..."):
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
    dtype_df = pd.DataFrame(dtype_report)
st.toast("AI schema analysis completed 🤖")

with st.container():
    st.write("## AI Data Type Detection & Recommendation")
    st.dataframe(dtype_df, use_container_width=True, hide_index=True)

st.divider()
col1, col2, col3 = st.columns(3)
col1.metric("Columns Reviewed", f"{len(dtype_df):,}")
col2.metric("High Confidence (>=90%)", f"{(dtype_df['Confidence'].str.rstrip('%').astype(float) >= 90).sum():,}")
col3.metric("Suggested Non-Object Types", f"{(dtype_df['AI Suggested Type'] != 'object').sum():,}")

with st.expander("Advanced: Current vs Suggested Type Summary"):
    summary_df = (
        dtype_df.groupby(["Current Data Type", "AI Suggested Type"])
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

csv = dtype_df.to_csv(index=False)
st.download_button(
    label="Download AI Schema Report",
    data=csv,
    file_name="ai_schema_report.csv",
    mime="text/csv"
)

footer()
