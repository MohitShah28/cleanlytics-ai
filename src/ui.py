import streamlit as st


def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 8% 0%, rgba(20, 184, 166, 0.10), transparent 33%),
            radial-gradient(circle at 92% 6%, rgba(245, 158, 11, 0.08), transparent 28%),
            linear-gradient(155deg, #0f141a 0%, #121923 56%, #0f141a 100%);
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        max-width: 1240px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d131a 0%, #131b25 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.14);
    }

    section[data-testid="stSidebar"] * {
        color: #e7ebf0;
    }

    div[data-testid="stSidebarNav"] > ul {
        gap: 2px;
    }

    div[data-testid="stSidebarNav"] a {
        border-radius: 10px;
        margin: 2px 0;
        transition: background 0.18s ease, border-color 0.18s ease;
        border: 1px solid transparent;
    }

    div[data-testid="stSidebarNav"] a:hover {
        background: rgba(20, 184, 166, 0.11);
        border-color: rgba(45, 212, 191, 0.20);
    }

    div[data-testid="stSidebarNav"] a[aria-current="page"] {
        background: linear-gradient(90deg, rgba(20, 184, 166, 0.18), rgba(245, 158, 11, 0.08));
        border-color: rgba(45, 212, 191, 0.30);
    }

    .hero-card {
        position: relative;
        overflow: hidden;
        background:
            linear-gradient(132deg, rgba(15, 21, 30, 0.97), rgba(22, 30, 41, 0.94));
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 18px;
        padding: 32px 34px;
        margin-bottom: 24px;
        box-shadow: 0 14px 34px rgba(0, 0, 0, 0.28);
        animation: fadeUp 0.8s ease both;
    }

    .hero-card::before {
        content: "";
        position: absolute;
        inset: -2px;
        background: linear-gradient(120deg, transparent, rgba(20, 184, 166, 0.08), transparent);
        transform: translateX(-100%);
        animation: shimmer 12s infinite;
    }

    .hero-content {
        position: relative;
        z-index: 2;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(20, 184, 166, 0.13);
        color: #5eead4;
        border: 1px solid rgba(45, 212, 191, 0.24);
        font-weight: 700;
        font-size: 13px;
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: 48px;
        line-height: 1.08;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1.1px;
        color: #f3f4f6;
    }

    .gradient-text {
        background: linear-gradient(90deg, #2dd4bf, #14b8a6, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #c8d0da;
        font-size: 17px;
        max-width: 760px;
        margin-top: 16px;
        line-height: 1.65;
    }

    .glass-card {
        background: rgba(18, 26, 36, 0.9);
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.22);
        backdrop-filter: blur(8px);
        animation: fadeUp 0.9s ease both;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }

    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(20, 184, 166, 0.34);
        box-shadow: 0 14px 30px rgba(20, 184, 166, 0.14);
    }

    .module-card {
        min-height: 190px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .module-icon {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        background: linear-gradient(135deg, rgba(20, 184, 166, 0.30), rgba(245, 158, 11, 0.22));
        border: 1px solid rgba(45, 212, 191, 0.24);
        margin-bottom: 14px;
    }

    .card-title {
        font-size: 21px;
        font-weight: 800;
        color: #f3f4f6;
        margin-bottom: 8px;
    }

    .card-text {
        font-size: 14px;
        color: #a3afbd;
        line-height: 1.6;
    }

    .section-title {
        font-size: 30px;
        font-weight: 800;
        color: #f3f4f6;
        margin: 30px 0 16px 0;
    }

    .workflow-step {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        padding: 14px 18px;
        border-radius: 18px;
        background: rgba(15,23,42,0.75);
        border: 1px solid rgba(148,163,184,0.15);
        margin: 6px;
        color: #e5e7eb;
        font-weight: 700;
    }

    .step-number {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: linear-gradient(135deg, #0d9488, #14b8a6);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
    }

    div[data-testid="stMetric"] {
        background: rgba(18, 26, 36, 0.92);
        border: 1px solid rgba(148, 163, 184, 0.14);
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 10px 24px rgba(0,0,0,0.22);
        animation: fadeUp 0.75s ease both;
    }

    div[data-testid="stMetric"]:hover {
        border-color: rgba(45, 212, 191, 0.36);
        transform: translateY(-2px);
        transition: all 0.25s ease;
    }

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 10px;
        border: 1px solid rgba(45, 212, 191, 0.45);
        background: linear-gradient(135deg, #0f766e, #14b8a6);
        color: white;
        font-weight: 700;
        padding: 0.65rem 1.1rem;
        transition: all 0.25s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(20, 184, 166, 0.34);
        border-color: rgba(94, 234, 212, 0.85);
    }

    .stDataFrame {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid rgba(148,163,184,0.13);
        animation: fadeUp 0.8s ease both;
    }

    div[data-testid="stFileUploader"] {
        background: rgba(18, 26, 36, 0.9);
        border: 1px dashed rgba(45, 212, 191, 0.38);
        border-radius: 12px;
        padding: 18px;
        animation: fadeUp 0.75s ease both;
    }

    .stAlert {
        border-radius: 10px;
    }

    .footer {
        margin-top: 40px;
        padding: 20px;
        text-align: center;
        color: #97a6b7;
        border-top: 1px solid rgba(148,163,184,0.15);
    }

    @keyframes fadeUp {
        from {
            opacity: 0;
            transform: translateY(18px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        45% { transform: translateX(100%); }
        100% { transform: translateX(100%); }
    }

    @media (max-width: 768px) {
        .hero-title {
            font-size: 36px;
        }
        .hero-card {
            padding: 28px;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def sidebar_branding():
    st.sidebar.markdown("## 🧹 Cleanlytics AI")
    st.sidebar.caption("AI-Powered Data Quality Platform")
    st.sidebar.divider()
    st.sidebar.markdown("### Modules")
    st.sidebar.markdown("""
    📊 Data Profiling  
    🤖 AI Schema Report  
    🧹 Data Cleaning  
    🚨 Outlier Detection  
    📄 Reports & Export  
    """)
    st.sidebar.divider()
    st.sidebar.info("Upload your dataset in Data Profiling first.")


def page_header(title, subtitle):
    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-content">
            <div class="hero-badge">⚡ AI-Powered</div>
            <h1 class="hero-title">{title}</h1>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def module_card(icon, title, text):
    st.markdown(f"""
    <div class="glass-card module-card">
        <div>
            <div class="module-icon">{icon}</div>
            <div class="card-title">{title}</div>
            <div class="card-text">{text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_title(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def footer():
    st.markdown("""
    <div class="footer">
        Cleanlytics AI · Built with Python, Streamlit, Pandas, Scikit-learn, and ReportLab
    </div>
    """, unsafe_allow_html=True)
