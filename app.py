import streamlit as st
from src.ui import (
    inject_custom_css,
    sidebar_branding,
    page_header,
    module_card,
    section_title,
    footer
)

st.set_page_config(
    page_title="Cleanlytics AI",
    page_icon="🧹",
    layout="wide"
)

inject_custom_css()
sidebar_branding()

page_header(
    "Welcome to <span class='gradient-text'>Cleanlytics AI</span>",
    "Profile, clean, validate, detect outliers, and export datasets safely using intelligent data-quality automation."
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Modules", "5")
col2.metric("Cleaning Engine", "Active")
col3.metric("AI Schema", "Enabled")
col4.metric("Reports", "PDF + CSV")

section_title("Platform Modules")

m1, m2, m3 = st.columns(3)
with m1:
    module_card("📊", "Data Profiling", "Upload datasets, preview records, view missing values, duplicates, and quality score.")
with m2:
    module_card("🤖", "AI Schema Report", "Get datatype suggestions with confidence scores and clear reasoning.")
with m3:
    module_card("🧹", "Data Cleaning", "Apply safe cleaning operations with datatype control and audit logs.")

m4, m5 = st.columns(2)
with m4:
    module_card("🚨", "Outlier Detection", "Detect abnormal numeric values using IQR, Z-score, and Isolation Forest.")
with m5:
    module_card("📄", "Reports & Export", "Download cleaned datasets, backups, reports, and professional PDF summaries.")

section_title("Recommended Workflow")

st.markdown("""
<div>
    <div class="workflow-step"><span class="step-number">1</span> Upload Dataset</div>
    <div class="workflow-step"><span class="step-number">2</span> Review AI Schema</div>
    <div class="workflow-step"><span class="step-number">3</span> Clean Data</div>
    <div class="workflow-step"><span class="step-number">4</span> Detect Outliers</div>
    <div class="workflow-step"><span class="step-number">5</span> Export Reports</div>
</div>
""", unsafe_allow_html=True)

st.info("Start by opening Data Profiling from the sidebar and uploading your CSV file.")

footer()
