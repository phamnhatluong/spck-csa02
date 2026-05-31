import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import uuid
from datetime import datetime
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
import warnings
warnings.filterwarnings("ignore")

# ─── COLOR HELPERS ────────────────────────────────────────────────────────────
def hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
    """Convert #rrggbb to rgba(r,g,b,a) — Plotly-safe."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c*2 for c in h)
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"

# ─── CONFIG ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IndustryLens",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

PUBLIC_DIR = "public_data"
os.makedirs(PUBLIC_DIR, exist_ok=True)

# ─── THEME PALETTES ───────────────────────────────────────────────────────────
THEMES = {
    "🌌 Dark Galaxy":  {
        "bg": "#0a0a0f", "surface": "#13131a", "surface2": "#1c1c28",
        "border": "#2a2a3a", "text": "#e8e8f0", "muted": "#6b6b85",
        "accent": "#7c6bff", "accent2": "#ff6b9d", "accent3": "#6bffce",
        "accent4": "#ffb347", "success": "#4ade80", "warning": "#fbbf24",
        "danger": "#f87171", "chart_colors": ["#7c6bff","#ff6b9d","#6bffce","#ffb347","#60a5fa","#f472b6","#34d399","#a78bfa"],
        "plotly_template": "plotly_dark",
    },
    "🌊 Ocean Depth": {
        "bg": "#020c18", "surface": "#061424", "surface2": "#0d2137",
        "border": "#1a3a5c", "text": "#cce8ff", "muted": "#5a8aaa",
        "accent": "#00d4ff", "accent2": "#0066ff", "accent3": "#00ffaa",
        "accent4": "#ff8800", "success": "#00e676", "warning": "#ffab40",
        "danger": "#ff5252", "chart_colors": ["#00d4ff","#0066ff","#00ffaa","#ff8800","#ff5252","#aa00ff","#64ffda","#40c4ff"],
        "plotly_template": "plotly_dark",
    },
    "🌸 Sakura Light": {
        "bg": "#fff5f7", "surface": "#ffffff", "surface2": "#fce4ec",
        "border": "#f8bbd0", "text": "#3d1a26", "muted": "#ad7989",
        "accent": "#e91e8c", "accent2": "#ff4081", "accent3": "#00bfa5",
        "accent4": "#ff6d00", "success": "#00c853", "warning": "#ff6d00",
        "danger": "#d50000", "chart_colors": ["#e91e8c","#ff4081","#00bfa5","#ff6d00","#6200ea","#00b0ff","#69f0ae","#ffab40"],
        "plotly_template": "plotly_white",
    },
    "🍃 Forest Calm": {
        "bg": "#f0f7f0", "surface": "#ffffff", "surface2": "#e8f5e9",
        "border": "#c8e6c9", "text": "#1b3a1f", "muted": "#5a8a62",
        "accent": "#2e7d32", "accent2": "#00897b", "accent3": "#f57f17",
        "accent4": "#1565c0", "success": "#43a047", "warning": "#fb8c00",
        "danger": "#e53935", "chart_colors": ["#2e7d32","#00897b","#f57f17","#1565c0","#6a1b9a","#ad1457","#558b2f","#00695c"],
        "plotly_template": "plotly_white",
    },
    "🔥 Cyberpunk": {
        "bg": "#0d0015", "surface": "#1a002b", "surface2": "#2a0045",
        "border": "#4a0080", "text": "#f0e0ff", "muted": "#9060c0",
        "accent": "#ff00ff", "accent2": "#00ffff", "accent3": "#ffff00",
        "accent4": "#ff6600", "success": "#00ff88", "warning": "#ffff00",
        "danger": "#ff0055", "chart_colors": ["#ff00ff","#00ffff","#ffff00","#ff6600","#00ff88","#ff0055","#aa00ff","#00aaff"],
        "plotly_template": "plotly_dark",
    },
    "☁️ Cloud White": {
        "bg": "#f8fafc", "surface": "#ffffff", "surface2": "#f1f5f9",
        "border": "#e2e8f0", "text": "#1e293b", "muted": "#94a3b8",
        "accent": "#3b82f6", "accent2": "#8b5cf6", "accent3": "#10b981",
        "accent4": "#f59e0b", "success": "#10b981", "warning": "#f59e0b",
        "danger": "#ef4444", "chart_colors": ["#3b82f6","#8b5cf6","#10b981","#f59e0b","#ef4444","#06b6d4","#84cc16","#f97316"],
        "plotly_template": "plotly_white",
    },
}

# ─── SESSION DEFAULTS ─────────────────────────────────────────────────────────
if "theme_name" not in st.session_state:
    st.session_state.theme_name = "🌌 Dark Galaxy"
if "df" not in st.session_state:
    st.session_state.df = None
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "published" not in st.session_state:
    st.session_state.published = False

T = THEMES[st.session_state.theme_name]

# ─── INJECT GLOBAL CSS ────────────────────────────────────────────────────────
def inject_css(t):
    is_dark = t["bg"] < "#888888"
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&family=Outfit:wght@300;400;500;600;700&display=swap');

    /* ── Global Reset ── */
    html, body, [class*="css"] {{
        font-family: 'Outfit', sans-serif !important;
        color: {t['text']} !important;
    }}
    .stApp {{
        background: {t['bg']} !important;
    }}

    /* ── Hide default streamlit chrome ── */
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px !important;
    }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background: {t['surface']} !important;
        border-right: 1px solid {t['border']} !important;
    }}
    [data-testid="stSidebar"] * {{
        color: {t['text']} !important;
    }}
    [data-testid="stSidebarContent"] {{
        padding: 1.5rem 1rem !important;
    }}

    /* ── Selectbox / Input ── */
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stTextArea textarea {{
        background: {t['surface2']} !important;
        border: 1px solid {t['border']} !important;
        color: {t['text']} !important;
        border-radius: 10px !important;
        font-family: 'Outfit', sans-serif !important;
    }}
    .stSelectbox [data-baseweb="select"] > div {{
        background: {t['surface2']} !important;
        border-color: {t['border']} !important;
        border-radius: 10px !important;
    }}

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {{
        background: {t['surface']} !important;
        border: 2px dashed {t['border']} !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        transition: border-color .3s !important;
    }}
    [data-testid="stFileUploader"]:hover {{
        border-color: {t['accent']} !important;
    }}
    [data-testid="stFileUploadDropzone"] {{
        background: transparent !important;
    }}

    /* ── Buttons ── */
    .stButton > button {{
        background: {t['accent']} !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: .9rem !important;
        padding: .6rem 1.6rem !important;
        transition: all .2s !important;
        box-shadow: 0 4px 15px {t['accent']}44 !important;
    }}
    .stButton > button:hover {{
        opacity: .88 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px {t['accent']}66 !important;
    }}

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {{
        background: {t['surface']} !important;
        border-radius: 12px !important;
        padding: .3rem !important;
        gap: .3rem !important;
        border: 1px solid {t['border']} !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent !important;
        border-radius: 8px !important;
        color: {t['muted']} !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        padding: .5rem 1.2rem !important;
        border: none !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: {t['accent']} !important;
        color: #fff !important;
    }}
    .stTabs [data-baseweb="tab-panel"] {{
        background: transparent !important;
        padding-top: 1.5rem !important;
    }}

    /* ── Metrics ── */
    [data-testid="stMetric"] {{
        background: {t['surface']} !important;
        border: 1px solid {t['border']} !important;
        border-radius: 14px !important;
        padding: 1.2rem 1.4rem !important;
        border-top: 3px solid {t['accent']} !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {t['muted']} !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: .72rem !important;
        text-transform: uppercase !important;
        letter-spacing: .06em !important;
    }}
    [data-testid="stMetricValue"] {{
        color: {t['text']} !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.7rem !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricDelta"] {{
        font-family: 'Outfit', sans-serif !important;
        font-size: .8rem !important;
    }}

    /* ── Expander ── */
    .streamlit-expanderHeader {{
        background: {t['surface']} !important;
        border: 1px solid {t['border']} !important;
        border-radius: 10px !important;
        color: {t['text']} !important;
        font-weight: 600 !important;
    }}
    .streamlit-expanderContent {{
        background: {t['surface2']} !important;
        border: 1px solid {t['border']} !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
    }}

    /* ── Spinner ── */
    .stSpinner > div {{
        border-top-color: {t['accent']} !important;
    }}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: {t['surface']}; }}
    ::-webkit-scrollbar-thumb {{ background: {t['border']}; border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {t['accent']}; }}

    /* ── Radio buttons ── */
    .stRadio [data-testid="stMarkdownContainer"] p {{
        color: {t['text']} !important;
    }}

    /* ── Divider ── */
    hr {{
        border-color: {t['border']} !important;
        margin: 1.5rem 0 !important;
    }}

    /* ── Success / Warning / Error boxes ── */
    .stSuccess, .stInfo, .stWarning, .stError {{
        border-radius: 10px !important;
        font-family: 'Outfit', sans-serif !important;
    }}

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {{
        border: 1px solid {t['border']} !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }}

    /* ── Custom card class ── */
    .lens-card {{
        background: {t['surface']};
        border: 1px solid {t['border']};
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
    }}
    .lens-card-accent {{
        border-top: 3px solid {t['accent']};
    }}

    /* ── Insight cards ── */
    .insight-success {{
        background: {t['success']}18;
        border: 1px solid {t['success']}55;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: .7rem;
    }}
    .insight-warning {{
        background: {t['warning']}18;
        border: 1px solid {t['warning']}55;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: .7rem;
    }}
    .insight-danger {{
        background: {t['danger']}18;
        border: 1px solid {t['danger']}55;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: .7rem;
    }}
    .insight-info {{
        background: {t['accent']}18;
        border: 1px solid {t['accent']}55;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: .7rem;
    }}

    /* ── Hero section ── */
    .hero-title {{
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: clamp(2rem, 4vw, 3.2rem);
        line-height: 1.1;
        letter-spacing: -.03em;
        color: {t['text']};
        margin-bottom: .5rem;
    }}
    .hero-accent {{
        color: {t['accent']};
    }}
    .hero-sub {{
        font-family: 'Outfit', sans-serif;
        color: {t['muted']};
        font-size: 1.05rem;
        line-height: 1.7;
        margin-bottom: 1.5rem;
    }}
    .badge {{
        display: inline-block;
        background: {t['accent']}22;
        color: {t['accent']};
        border: 1px solid {t['accent']}55;
        border-radius: 20px;
        padding: .25rem .9rem;
        font-size: .75rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: .05em;
        margin-bottom: 1rem;
    }}
    .section-header {{
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 1.25rem;
        color: {t['text']};
        margin-bottom: 1rem;
        padding-bottom: .5rem;
        border-bottom: 2px solid {t['border']};
    }}
    .kpi-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-size: .7rem;
        color: {t['muted']};
        text-transform: uppercase;
        letter-spacing: .08em;
    }}
    .public-card {{
        background: {t['surface']};
        border: 1px solid {t['border']};
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: .8rem;
        transition: border-color .2s;
        cursor: pointer;
    }}
    .public-card:hover {{
        border-color: {t['accent']};
    }}
    .tag-pill {{
        display: inline-block;
        background: {t['accent']}22;
        color: {t['accent']};
        border-radius: 20px;
        padding: .2rem .7rem;
        font-size: .75rem;
        font-weight: 600;
        margin: .15rem;
    }}
    </style>
    """, unsafe_allow_html=True)

inject_css(T)

# ─── ANALYSIS ENGINE ──────────────────────────────────────────────────────────
def safe_json(d):
    if isinstance(d, dict):  return {k: safe_json(v) for k, v in d.items()}
    if isinstance(d, list):  return [safe_json(i) for i in d]
    if isinstance(d, float) and (np.isnan(d) or np.isinf(d)): return None
    if isinstance(d, (np.integer,)): return int(d)
    if isinstance(d, (np.floating,)): return float(d)
    return d

def analyze(df: pd.DataFrame) -> dict:
    R = {}
    R["total_records"] = len(df)
    R["columns"] = df.columns.tolist()
    R["industries"] = df["industry"].dropna().unique().tolist() if "industry" in df.columns else []
    R["regions"]    = df["region"].dropna().unique().tolist() if "region" in df.columns else []
    R["job_titles"] = df["job_title"].dropna().unique().tolist() if "job_title" in df.columns else []

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"]).sort_values("date")
        df["_period"] = df["date"].dt.to_period("M")
        df["_ts"]     = (df["date"] - df["date"].min()).dt.days

    # ── Trends ──
    trends = {}
    for col, agg in [("job_openings","sum"), ("avg_salary","mean"), ("growth_score","mean")]:
        if col in df.columns and "date" in df.columns:
            g = df.groupby("_period")[col].agg(agg).reset_index()
            g["date"] = g["_period"].dt.to_timestamp()
            if len(g) >= 3 and col == "job_openings":
                X = ((g["date"] - g["date"].min()).dt.days).values.reshape(-1,1)
                m = LinearRegression().fit(X, g[col].values)
                trends["job_openings_slope"] = round(float(m.coef_[0]),4)
                trends["job_openings_trend"] = "tăng" if m.coef_[0] > 0 else "giảm"
            trends[f"{col}_monthly"] = {
                "labels": [str(d.date()) for d in g["date"]],
                "values": [round(float(v),2) for v in g[col]]
            }
    R["trends"] = trends

    # ── Forecast ──
    forecast = {}
    if "job_openings" in df.columns and "date" in df.columns:
        g = df.groupby("_period")["job_openings"].sum().reset_index()
        g["date"] = g["_period"].dt.to_timestamp()
        if len(g) >= 4:
            ts = (g["date"] - g["date"].min()).dt.days.values.reshape(-1,1)
            poly = PolynomialFeatures(degree=2)
            Xp = poly.fit_transform(ts)
            ridge = Ridge(alpha=1.0).fit(Xp, g["job_openings"].values)
            last_ts  = float(ts.max())
            last_dt  = g["date"].max()
            f_days   = np.array([last_ts + 30*i for i in range(1,7)]).reshape(-1,1)
            f_preds  = ridge.predict(poly.transform(f_days))
            forecast["job_openings"] = {
                "labels": [str((last_dt + pd.DateOffset(months=i)).date()) for i in range(1,7)],
                "values": [max(0, round(float(v),0)) for v in f_preds]
            }

    if "avg_salary" in df.columns and "salary_growth_rate" in df.columns:
        gr = float(df["salary_growth_rate"].mean())
        cs = float(df["avg_salary"].mean())
        forecast["salary"] = {
            "labels": [f"Tháng +{i}" for i in range(1,7)],
            "values": [round(cs * (1+gr/100)**i, 2) for i in range(1,7)]
        }

    if "growth_score" in df.columns:
        gs = float(df["growth_score"].mean())
        forecast["growth_score"] = {
            "mean": round(gs,2),
            "std":  round(float(df["growth_score"].std()),2),
            "outlook": "Tích cực 🟢" if gs>60 else ("Trung bình 🟡" if gs>40 else "Thận trọng 🔴")
        }
    R["forecast"] = forecast

    # ── Distributions ──
    dists = {}
    for col in ["experience_level","competition_level","automation_risk","demand_forecast"]:
        if col in df.columns:
            vc = df[col].value_counts()
            dists[col] = {"labels": vc.index.tolist(), "values": vc.values.tolist()}

    if "remote_ratio" in df.columns:
        bins = [0,20,40,60,80,100]
        labels = ["0–20%","21–40%","41–60%","61–80%","81–100%"]
        counts = pd.cut(df["remote_ratio"], bins=bins, labels=labels).value_counts().reindex(labels).fillna(0)
        dists["remote_ratio"] = {
            "mean": round(float(df["remote_ratio"].mean()),1),
            "bins": labels,
            "values": counts.astype(int).tolist()
        }

    if "job_title" in df.columns and "avg_salary" in df.columns:
        tj = df.groupby("job_title")["avg_salary"].mean().nlargest(8)
        dists["top_paying_jobs"] = {"labels": tj.index.tolist(), "values": [round(float(v),2) for v in tj.values]}

    if "region" in df.columns and "job_openings" in df.columns:
        rj = df.groupby("region")["job_openings"].sum().nlargest(8)
        dists["jobs_by_region"] = {"labels": rj.index.tolist(), "values": [int(v) for v in rj.values]}

    if "required_skills" in df.columns:
        skills = df["required_skills"].dropna().str.split(",").explode().str.strip().value_counts().head(12)
        dists["top_skills"] = {"labels": skills.index.tolist(), "values": skills.values.tolist()}

    if "job_title" in df.columns and "job_openings" in df.columns:
        jt = df.groupby("job_title")["job_openings"].sum().nlargest(8)
        dists["openings_by_title"] = {"labels": jt.index.tolist(), "values": [int(v) for v in jt.values]}

    R["distributions"] = dists

    # ── KPIs ──
    R["kpis"] = {
        "avg_salary":       round(float(df["avg_salary"].mean()),2) if "avg_salary" in df.columns else None,
        "total_openings":   int(df["job_openings"].sum()) if "job_openings" in df.columns else None,
        "avg_growth_score": round(float(df["growth_score"].mean()),1) if "growth_score" in df.columns else None,
        "avg_salary_growth":round(float(df["salary_growth_rate"].mean()),2) if "salary_growth_rate" in df.columns else None,
        "avg_remote":       round(float(df["remote_ratio"].mean()),1) if "remote_ratio" in df.columns else None,
        "industry":         df["industry"].mode()[0] if "industry" in df.columns and len(df)>0 else "N/A",
    }

    # ── Insights ──
    insights = []
    if "automation_risk" in df.columns and df["automation_risk"].dtype == object:
        hr = (df["automation_risk"].str.lower()=="high").mean()*100
        if hr > 40:
            insights.append({"type":"warning","icon":"⚠️","title":"Rủi ro tự động hóa cao","desc":f"{hr:.0f}% vị trí có nguy cơ bị AI thay thế. Nên đầu tư vào kỹ năng sáng tạo & quản lý."})
        else:
            insights.append({"type":"success","icon":"🛡️","title":"Ngành an toàn trước AI","desc":f"Chỉ {hr:.0f}% rủi ro cao — ngành này còn nhiều dư địa phát triển."})

    if "remote_ratio" in df.columns:
        ar = df["remote_ratio"].mean()
        if ar > 60:
            insights.append({"type":"info","icon":"🌐","title":"Xu hướng Remote mạnh","desc":f"Tỷ lệ remote TB {ar:.0f}%. Cơ hội tuyển dụng toàn cầu."})
        elif ar < 25:
            insights.append({"type":"info","icon":"🏢","title":"Văn hóa làm việc trực tiếp","desc":f"Remote chỉ {ar:.0f}% — ngành yêu cầu hiện diện thực tế cao."})

    if "growth_score" in df.columns:
        gs = df["growth_score"].mean()
        if gs > 65:
            insights.append({"type":"success","icon":"🚀","title":"Ngành tăng trưởng mạnh","desc":f"Điểm tăng trưởng TB {gs:.1f}/100 — thời điểm vàng để đầu tư nhân lực."})
        elif gs < 40:
            insights.append({"type":"danger","icon":"📉","title":"Tăng trưởng chậm","desc":f"Điểm {gs:.1f}/100. Cân nhắc chiến lược đa dạng hóa."})

    if "salary_growth_rate" in df.columns:
        sgr = df["salary_growth_rate"].mean()
        if sgr > 8:
            insights.append({"type":"success","icon":"💰","title":"Lương tăng trưởng xuất sắc","desc":f"TB {sgr:.1f}%/năm — ngành hấp dẫn nhân tài hàng đầu."})
        elif sgr > 4:
            insights.append({"type":"info","icon":"💵","title":"Lương tăng ổn định","desc":f"TB {sgr:.1f}%/năm — duy trì sức hút với ứng viên tốt."})

    if "competition_level" in df.columns and df["competition_level"].dtype == object:
        hc = (df["competition_level"].str.lower()=="high").mean()*100
        if hc > 50:
            insights.append({"type":"warning","icon":"⚔️","title":"Cạnh tranh gay gắt","desc":f"{hc:.0f}% vị trí cạnh tranh cao. Cần xây dựng employer brand mạnh."})

    R["insights"] = insights
    return safe_json(R)

# ─── PLOTLY HELPERS ───────────────────────────────────────────────────────────
def pgo(title=""):
    return dict(
        template=T["plotly_template"],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Outfit, sans-serif", color=T["text"], size=12),
        title=dict(text=title, font=dict(family="Syne, sans-serif", size=15, color=T["text"]), x=0, pad=dict(l=0)),
        margin=dict(l=10, r=10, t=40 if title else 10, b=10),
        colorway=T["chart_colors"],
        legend=dict(font=dict(color=T["muted"], size=11)),
        xaxis=dict(gridcolor=T["border"], tickfont=dict(color=T["muted"]), linecolor=T["border"]),
        yaxis=dict(gridcolor=T["border"], tickfont=dict(color=T["muted"]), linecolor=T["border"]),
    )

def fmt_num(n, pre=""):
    if n is None: return "N/A"
    if n >= 1e9:  return f"{pre}{n/1e9:.1f}B"
    if n >= 1e6:  return f"{pre}{n/1e6:.1f}M"
    if n >= 1e3:  return f"{pre}{n/1e3:.1f}K"
    return f"{pre}{n:,.0f}"

# ─── CHART RENDERERS ──────────────────────────────────────────────────────────
def chart_line(labels, values, title, color=None):
    color = color or T["accent"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=labels, y=values, mode="lines+markers",
        line=dict(color=color, width=2.5),
        marker=dict(color=color, size=6),
        fill="tozeroy", fillcolor=hex_to_rgba(color, 0.13),
        hovertemplate="%{x}<br><b>%{y:,.0f}</b><extra></extra>"
    ))
    fig.update_layout(**pgo(title))
    return fig

def chart_bar(labels, values, title, color=None, horizontal=False):
    color = color or T["accent"]
    if horizontal:
        fig = go.Figure(go.Bar(
            x=values, y=labels, orientation="h",
            marker=dict(color=T["chart_colors"][:len(labels)], line=dict(width=0)),
            hovertemplate="%{y}<br><b>%{x:,.0f}</b><extra></extra>"
        ))
        fig.update_layout(**{**pgo(title), "yaxis": dict(gridcolor=T["border"], tickfont=dict(color=T["muted"], size=11), autorange="reversed")})
    else:
        fig = go.Figure(go.Bar(
            x=labels, y=values,
            marker=dict(color=color, opacity=.85, line=dict(width=0)),
            hovertemplate="%{x}<br><b>%{y:,.0f}</b><extra></extra>"
        ))
        fig.update_layout(**pgo(title))
    return fig

def chart_donut(labels, values, title):
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=.55,
        marker=dict(colors=T["chart_colors"][:len(labels)], line=dict(color=T["bg"], width=2)),
        textfont=dict(color=T["text"], size=12),
        hovertemplate="%{label}<br><b>%{value}</b> (%{percent})<extra></extra>"
    ))
    fig.update_layout(**{**pgo(title), "showlegend": True,
        "legend": dict(font=dict(color=T["muted"], size=11), orientation="v", x=1.02)})
    return fig

def chart_scatter(df, title):
    if "avg_salary" not in df.columns or "growth_score" not in df.columns:
        return None
    color_col = "experience_level" if "experience_level" in df.columns else None
    fig = px.scatter(
        df.sample(min(500, len(df))),
        x="avg_salary", y="growth_score",
        color=color_col,
        size="job_openings" if "job_openings" in df.columns else None,
        hover_data=[c for c in ["job_title","region","industry"] if c in df.columns],
        color_discrete_sequence=T["chart_colors"],
        title=title,
        labels={"avg_salary":"Lương TB ($)","growth_score":"Điểm tăng trưởng"},
    )
    fig.update_layout(**pgo(title))
    return fig

def chart_heatmap(df):
    num_cols = [c for c in ["avg_salary","job_openings","growth_score","salary_growth_rate","remote_ratio"] if c in df.columns]
    if len(num_cols) < 2: return None
    corr = df[num_cols].corr()
    labels_vi = {
        "avg_salary":"Lương TB","job_openings":"Tuyển dụng",
        "growth_score":"Tăng trưởng","salary_growth_rate":"Tăng lương %","remote_ratio":"Remote %"
    }
    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=[labels_vi.get(c,c) for c in corr.columns],
        y=[labels_vi.get(c,c) for c in corr.index],
        colorscale=[[0,T["danger"]],[0.5,T["surface2"]],[1,T["accent"]]],
        text=np.round(corr.values,2),
        texttemplate="%{text}",
        hovertemplate="%{y} × %{x}<br>r = %{z:.3f}<extra></extra>",
        zmin=-1, zmax=1,
    ))
    fig.update_layout(**pgo("Ma trận tương quan"))
    return fig

def chart_salary_dist(df):
    if "avg_salary" not in df.columns: return None
    group_col = "experience_level" if "experience_level" in df.columns else None
    if group_col:
        fig = go.Figure()
        for i, lvl in enumerate(df[group_col].dropna().unique()):
            vals = df[df[group_col]==lvl]["avg_salary"]
            fig.add_trace(go.Box(
                x=[lvl]*len(vals), y=vals,
                name=str(lvl),
                marker_color=T["chart_colors"][i % len(T["chart_colors"])],
                boxmean=True,
                hovertemplate=f"<b>{lvl}</b><br>%{{y:,.0f}}<extra></extra>"
            ))
        fig.update_layout(**pgo("Phân phối lương theo cấp độ"))
    else:
        fig = px.histogram(df, x="avg_salary", nbins=30, color_discrete_sequence=[T["accent"]], title="Phân phối lương")
        fig.update_layout(**pgo("Phân phối lương"))
    return fig

def chart_timeline_multi(A):
    """Overlay job_openings + growth_score on dual y-axis"""
    t = A.get("trends",{})
    if "job_openings_monthly" not in t or "growth_score_monthly" not in t:
        return None
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    jd = t["job_openings_monthly"]
    gs = t["growth_score_monthly"]
    fig.add_trace(go.Bar(x=jd["labels"], y=jd["values"], name="Tuyển dụng",
        marker_color=hex_to_rgba(T["accent"], 0.73), hovertemplate="%{x}<br>Tuyển: <b>%{y:,.0f}</b><extra></extra>"), secondary_y=False)
    fig.add_trace(go.Scatter(x=gs["labels"], y=gs["values"], name="Growth Score",
        line=dict(color=T["accent2"],width=2.5), mode="lines+markers",
        marker=dict(size=5), hovertemplate="%{x}<br>Score: <b>%{y:.1f}</b><extra></extra>"), secondary_y=True)
    opts = pgo("Tuyển dụng & Điểm tăng trưởng")
    opts["yaxis2"] = dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(color=T["muted"]), title="Growth Score")
    opts["legend"] = dict(orientation="h", y=-0.15, font=dict(color=T["muted"],size=11))
    fig.update_layout(**opts)
    return fig

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding: .5rem 0 1.5rem;">
        <div style="font-family:'Syne',sans-serif; font-weight:800; font-size:1.5rem; color:{T['text']};">
            Industry<span style="color:{T['accent']}">Lens</span>
        </div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:.65rem; color:{T['muted']}; margin-top:.3rem;">
            v2.0 · Streamlit Edition
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="section-header">🎨 Chủ đề màu sắc</div>', unsafe_allow_html=True)
    new_theme = st.selectbox(
        "Chọn theme",
        list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.theme_name),
        label_visibility="collapsed"
    )
    if new_theme != st.session_state.theme_name:
        st.session_state.theme_name = new_theme
        st.rerun()

    # Color preview dots
    cols_preview = st.columns(4)
    for i, (label, color) in enumerate(zip(
        ["Chính","Phụ 1","Phụ 2","Phụ 3"],
        [T["accent"], T["accent2"], T["accent3"], T["accent4"]]
    )):
        cols_preview[i].markdown(f"""
        <div style="text-align:center;">
          <div style="width:28px;height:28px;border-radius:50%;background:{color};margin:0 auto 4px;border:2px solid {T['border']};"></div>
          <div style="font-size:.6rem;color:{T['muted']};">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Custom color picker
    with st.expander("🖌️ Tuỳ chỉnh màu chính"):
        custom_accent = st.color_picker("Màu nhấn", T["accent"])
        if custom_accent != T["accent"]:
            THEMES[st.session_state.theme_name]["accent"] = custom_accent
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">📂 Tải dữ liệu</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload file CSV / Excel",
        type=["csv","xlsx","xls"],
        label_visibility="collapsed"
    )
    uploader_name = st.text_input("Tên của bạn (tuỳ chọn)", placeholder="Ẩn danh", label_visibility="visible")

    if uploaded:
        if st.button("⚡ Phân tích ngay", use_container_width=True):
            with st.spinner("Đang phân tích dữ liệu..."):
                try:
                    if uploaded.name.endswith(".csv"):
                        df = pd.read_csv(uploaded)
                    else:
                        df = pd.read_excel(uploaded)
                    st.session_state.df = df
                    st.session_state.analysis = analyze(df)
                    st.session_state.analysis["uploader"] = uploader_name or "Ẩn danh"
                    st.session_state.analysis["uploaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    st.session_state.published = False
                    st.success(f"✅ Phân tích xong! {len(df):,} bản ghi.")
                except Exception as e:
                    st.error(f"❌ Lỗi: {e}")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Public reports nav
    public_files = []
    for f in os.listdir(PUBLIC_DIR):
        if f.endswith(".json"):
            try:
                with open(os.path.join(PUBLIC_DIR, f)) as fp:
                    meta = json.load(fp)
                public_files.append({"id": f.replace(".json",""), **meta.get("kpis",{}),
                    "total_records": meta.get("total_records",0),
                    "uploader": meta.get("uploader","Ẩn danh"),
                    "uploaded_at": meta.get("uploaded_at","")})
            except: pass

    if public_files:
        st.markdown(f'<div class="section-header">🌐 Báo cáo công khai ({len(public_files)})</div>', unsafe_allow_html=True)
        selected_public = st.selectbox(
            "Xem báo cáo",
            ["-- Chọn báo cáo --"] + [f"{p.get('industry','?')} · {p['uploader']} · {p['uploaded_at']}" for p in public_files],
            label_visibility="collapsed"
        )
        if selected_public != "-- Chọn báo cáo --":
            idx = [f"{p.get('industry','?')} · {p['uploader']} · {p['uploaded_at']}" for p in public_files].index(selected_public)
            fpath = os.path.join(PUBLIC_DIR, public_files[idx]["id"]+".json")
            try:
                with open(fpath) as fp:
                    pub_data = json.load(fp)
                    # load file if it has df backup, otherwise just show analysis
                    st.session_state.analysis = pub_data
                    st.session_state.df = None
                    st.success("📖 Đã tải báo cáo công khai!")
            except: pass

    st.markdown(f"""
    <div style="margin-top:2rem; padding:.8rem; background:{T['surface2']}; border-radius:10px; border:1px solid {T['border']};">
      <div style="font-family:'JetBrains Mono',monospace; font-size:.65rem; color:{T['muted']}; line-height:1.8;">
        📋 Các cột được hỗ trợ:<br>
        date · industry · job_title<br>
        region · job_openings<br>
        avg_salary · salary_growth_rate<br>
        experience_level · remote_ratio<br>
        required_skills · competition_level<br>
        automation_risk · growth_score<br>
        demand_forecast
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────
A = st.session_state.analysis
df_raw = st.session_state.df

if A is None:
    # ── Landing Hero ──
    st.markdown(f"""
    <div style="max-width:800px; margin: 4rem auto 0; text-align:center;">
      <div class="badge">🔬 AI-Powered Industry Intelligence</div>
      <div class="hero-title">Khám phá xu hướng<br><span class="hero-accent">ngành nghề tương lai</span></div>
      <p class="hero-sub">
        Tải lên dữ liệu CSV / Excel của bạn → Nhận ngay phân tích xu hướng,<br>
        dự báo tăng trưởng và chiến lược định hướng phát triển.
      </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, icon, title, desc in zip(
        [c1,c2,c3],
        ["📈","🔮","💡"],
        ["Xác định xu hướng","Dự báo tương lai","Đề xuất chiến lược"],
        ["Phát hiện quy luật tăng/giảm từ dữ liệu lịch sử",
         "Dự đoán tuyển dụng & lương 6 tháng tới",
         "Nhận định thực tế giúp định hướng phát triển"]
    ):
        col.markdown(f"""
        <div class="lens-card lens-card-accent" style="text-align:center; padding:2rem 1.5rem;">
          <div style="font-size:2.2rem; margin-bottom:.8rem;">{icon}</div>
          <div style="font-family:'Syne',sans-serif; font-weight:700; font-size:1rem; color:{T['text']}; margin-bottom:.5rem;">{title}</div>
          <div style="font-size:.85rem; color:{T['muted']}; line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center; margin-top:3rem; color:{T['muted']}; font-size:.9rem;">
        ← Tải file CSV/Excel lên từ sidebar để bắt đầu
    </div>
    """, unsafe_allow_html=True)

else:
    # ── Header Bar ──
    kpis = A.get("kpis", {})
    col_h1, col_h2 = st.columns([1,1])
    with col_h1:
        st.markdown(f"""
        <div style="padding:.5rem 0;">
          <div class="badge">📊 {kpis.get('industry','Ngành nghề')} · {A.get('total_records',0):,} bản ghi</div>
          <div class="hero-title" style="font-size:2rem;">Dashboard Phân Tích</div>
          <div style="font-size:.85rem; color:{T['muted']};">
            👤 {A.get('uploader','—')} &nbsp;·&nbsp; 🕒 {A.get('uploaded_at','—')}
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col_h2:
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if not st.session_state.published:
                if st.button("🌐 Chia sẻ công khai", use_container_width=True):
                    fid = str(uuid.uuid4())[:8]
                    fpath = os.path.join(PUBLIC_DIR, f"{fid}.json")
                    with open(fpath,"w",encoding="utf-8") as fp:
                        json.dump(A, fp, ensure_ascii=False, indent=2)
                    st.session_state.published = True
                    st.success(f"✅ Đã đăng công khai! ID: `{fid}`")
            else:
                st.success("✅ Đã công khai rồi!")
        with btn_c2:
            json_str = json.dumps(A, ensure_ascii=False, indent=2)
            st.download_button("⬇️ Tải báo cáo JSON", json_str, "report.json", "application/json", use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── KPI Strip ──
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: st.metric("💼 Lương TB", fmt_num(kpis.get("avg_salary"),"$"))
    with k2: st.metric("📋 Tổng tuyển dụng", fmt_num(kpis.get("total_openings")))
    with k3: st.metric("🚀 Điểm tăng trưởng", f"{kpis.get('avg_growth_score','—')}/100")
    with k4: st.metric("💹 Tăng lương", f"{kpis.get('avg_salary_growth','—')}%")
    with k5: st.metric("🌐 Remote TB", f"{kpis.get('avg_remote','—')}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TABS ──
    tabs = st.tabs(["📈 Xu hướng", "🔮 Dự báo", "📊 Phân phối", "🔬 Phân tích nâng cao", "💡 Chiến lược", "📋 Dữ liệu"])

    # ════════════════════════════════════════════════════════════
    # TAB 1 — TRENDS
    # ════════════════════════════════════════════════════════════
    with tabs[0]:
        trends = A.get("trends", {})
        st.markdown(f'<div class="section-header">📈 Xu hướng theo thời gian</div>', unsafe_allow_html=True)

        if trends.get("job_openings_trend"):
            direction = trends["job_openings_trend"]
            icon = "📈" if direction=="tăng" else "📉"
            color_box = T["success"] if direction=="tăng" else T["danger"]
            st.markdown(f"""
            <div style="background:{color_box}18; border:1px solid {color_box}55; border-radius:10px; padding:.8rem 1.2rem; margin-bottom:1.2rem; display:inline-block;">
              {icon} Xu hướng tuyển dụng đang <b style="color:{color_box};">{direction}</b>
              &nbsp;(hệ số: {trends.get('job_openings_slope',0):+.2f} vị trí/ngày)
            </div>
            """, unsafe_allow_html=True)

        row1_c1, row1_c2 = st.columns(2)
        with row1_c1:
            if "job_openings_monthly" in trends:
                d = trends["job_openings_monthly"]
                fig = chart_line(d["labels"], d["values"], "📋 Tuyển dụng theo tháng", T["accent"])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Không có cột `job_openings` hoặc `date`")

        with row1_c2:
            if "avg_salary_monthly" in trends:
                d = trends["avg_salary_monthly"]
                fig = chart_line(d["labels"], d["values"], "💰 Lương TB theo tháng", T["accent2"])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Không có cột `avg_salary` hoặc `date`")

        row2_c1, row2_c2 = st.columns(2)
        with row2_c1:
            if "growth_score_monthly" in trends:
                d = trends["growth_score_monthly"]
                fig = chart_line(d["labels"], d["values"], "🚀 Điểm tăng trưởng theo tháng", T["accent3"])
                st.plotly_chart(fig, use_container_width=True)

        with row2_c2:
            fig_dual = chart_timeline_multi(A)
            if fig_dual:
                st.plotly_chart(fig_dual, use_container_width=True)

    # ════════════════════════════════════════════════════════════
    # TAB 2 — FORECAST
    # ════════════════════════════════════════════════════════════
    with tabs[1]:
        fc = A.get("forecast", {})
        st.markdown(f'<div class="section-header">🔮 Dự báo 6 tháng tới</div>', unsafe_allow_html=True)

        # Growth score card
        if "growth_score" in fc:
            gs = fc["growth_score"]
            color_gs = T["success"] if "Tích cực" in gs["outlook"] else (T["warning"] if "Trung bình" in gs["outlook"] else T["danger"])
            st.markdown(f"""
            <div style="background:{T['surface']}; border:1px solid {T['border']}; border-radius:16px; padding:1.8rem 2rem; margin-bottom:1.5rem; display:flex; align-items:center; gap:2rem; flex-wrap:wrap;">
              <div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:.7rem; color:{T['muted']}; text-transform:uppercase; letter-spacing:.08em;">Điểm tăng trưởng trung bình</div>
                <div style="font-family:'Syne',sans-serif; font-size:3rem; font-weight:800; color:{T['text']};">{gs['mean']}<span style="font-size:1.2rem; color:{T['muted']};">/100</span></div>
                <div style="font-size:.85rem; color:{T['muted']};">Độ lệch chuẩn: ±{gs['std']}</div>
              </div>
              <div style="background:{color_gs}22; border:1px solid {color_gs}55; border-radius:12px; padding:.8rem 1.5rem;">
                <div style="font-family:'Syne',sans-serif; font-weight:700; font-size:1.1rem; color:{color_gs};">Triển vọng: {gs['outlook']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        fc_c1, fc_c2 = st.columns(2)
        with fc_c1:
            if "job_openings" in fc:
                d = fc["job_openings"]
                fig = chart_bar(d["labels"], d["values"], "📋 Dự báo tuyển dụng", T["accent4"])
                st.plotly_chart(fig, use_container_width=True)
                # table
                fc_df = pd.DataFrame({"Tháng": d["labels"], "Dự báo tuyển dụng": [int(v) for v in d["values"]]})
                st.dataframe(fc_df, use_container_width=True, hide_index=True)
            else:
                st.info("Cần ít nhất 4 tháng dữ liệu để dự báo tuyển dụng.")

        with fc_c2:
            if "salary" in fc:
                d = fc["salary"]
                fig = chart_line(d["labels"], d["values"], "💰 Dự báo lương", T["accent2"])
                st.plotly_chart(fig, use_container_width=True)
                fc_df2 = pd.DataFrame({"Tháng": d["labels"], "Lương dự báo ($)": [f"${v:,.0f}" for v in d["values"]]})
                st.dataframe(fc_df2, use_container_width=True, hide_index=True)
            else:
                st.info("Cần cột `avg_salary` và `salary_growth_rate` để dự báo lương.")

    # ════════════════════════════════════════════════════════════
    # TAB 3 — DISTRIBUTIONS
    # ════════════════════════════════════════════════════════════
    with tabs[2]:
        dist = A.get("distributions", {})
        st.markdown(f'<div class="section-header">📊 Phân phối & thống kê</div>', unsafe_allow_html=True)

        row_d1, row_d2, row_d3 = st.columns(3)
        with row_d1:
            if "experience_level" in dist:
                d = dist["experience_level"]
                st.plotly_chart(chart_donut(d["labels"], d["values"], "👥 Cấp độ kinh nghiệm"), use_container_width=True)
        with row_d2:
            if "competition_level" in dist:
                d = dist["competition_level"]
                st.plotly_chart(chart_donut(d["labels"], d["values"], "⚔️ Mức cạnh tranh"), use_container_width=True)
        with row_d3:
            if "automation_risk" in dist:
                d = dist["automation_risk"]
                st.plotly_chart(chart_donut(d["labels"], d["values"], "🤖 Rủi ro AI"), use_container_width=True)

        row_d4, row_d5 = st.columns(2)
        with row_d4:
            if "top_paying_jobs" in dist:
                d = dist["top_paying_jobs"]
                st.plotly_chart(chart_bar(d["labels"], d["values"], "💼 Top vị trí lương cao nhất", horizontal=True), use_container_width=True)
        with row_d5:
            if "top_skills" in dist:
                d = dist["top_skills"]
                st.plotly_chart(chart_bar(d["labels"], d["values"], "🛠️ Kỹ năng được yêu cầu nhiều nhất", horizontal=True), use_container_width=True)

        row_d6, row_d7 = st.columns(2)
        with row_d6:
            if "jobs_by_region" in dist:
                d = dist["jobs_by_region"]
                st.plotly_chart(chart_bar(d["labels"], d["values"], "🗺️ Tuyển dụng theo khu vực", T["accent3"]), use_container_width=True)
        with row_d7:
            if "demand_forecast" in dist:
                d = dist["demand_forecast"]
                st.plotly_chart(chart_donut(d["labels"], d["values"], "📡 Phân bố nhu cầu dự báo"), use_container_width=True)

        if "remote_ratio" in dist:
            rd = dist["remote_ratio"]
            st.markdown(f"""
            <div class="lens-card" style="margin-bottom:1rem;">
              <span style="font-family:'JetBrains Mono',monospace; font-size:.7rem; color:{T['muted']};">REMOTE RATIO TRUNG BÌNH</span>
              <span style="font-size:1.6rem; font-weight:700; font-family:'JetBrains Mono',monospace; margin-left:1rem;">{rd['mean']}%</span>
            </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(
                chart_bar(rd["bins"], rd["values"], "🌐 Phân bố tỷ lệ làm việc từ xa", T["accent2"]),
                use_container_width=True
            )

    # ════════════════════════════════════════════════════════════
    # TAB 4 — ADVANCED ANALYSIS
    # ════════════════════════════════════════════════════════════
    with tabs[3]:
        st.markdown(f'<div class="section-header">🔬 Phân tích nâng cao</div>', unsafe_allow_html=True)

        if df_raw is not None:
            adv_c1, adv_c2 = st.columns(2)
            with adv_c1:
                fig_s = chart_scatter(df_raw, "💹 Tương quan Lương & Điểm tăng trưởng")
                if fig_s:
                    st.plotly_chart(fig_s, use_container_width=True)
                else:
                    st.info("Cần cột `avg_salary` và `growth_score`.")

            with adv_c2:
                fig_b = chart_salary_dist(df_raw)
                if fig_b:
                    st.plotly_chart(fig_b, use_container_width=True)
                else:
                    st.info("Cần cột `avg_salary`.")

            fig_h = chart_heatmap(df_raw)
            if fig_h:
                st.plotly_chart(fig_h, use_container_width=True)

            # Salary by region
            if "region" in df_raw.columns and "avg_salary" in df_raw.columns:
                region_sal = df_raw.groupby("region")["avg_salary"].mean().reset_index().sort_values("avg_salary", ascending=False)
                fig_rs = px.bar(region_sal, x="region", y="avg_salary",
                    color="avg_salary", color_continuous_scale=[[0,hex_to_rgba(T["accent"], 0.4)],[1,T["accent"]]],
                    labels={"region":"Khu vực","avg_salary":"Lương TB ($)"},
                    title="🗺️ Lương trung bình theo khu vực")
                fig_rs.update_layout(**pgo())
                fig_rs.update_coloraxes(showscale=False)
                st.plotly_chart(fig_rs, use_container_width=True)

            # Salary growth over time
            if "date" in df_raw.columns and "salary_growth_rate" in df_raw.columns:
                df_tmp = df_raw.copy()
                df_tmp["date"] = pd.to_datetime(df_tmp["date"], errors="coerce")
                df_tmp = df_tmp.dropna(subset=["date"])
                g = df_tmp.groupby(df_tmp["date"].dt.to_period("M"))["salary_growth_rate"].mean().reset_index()
                g["date"] = g["date"].dt.to_timestamp()
                fig_sg = chart_line([str(d.date()) for d in g["date"]], g["salary_growth_rate"].tolist(),
                    "📈 Tốc độ tăng lương theo tháng (%)", T["accent4"])
                st.plotly_chart(fig_sg, use_container_width=True)
        else:
            st.info("📁 Tải file dữ liệu lên để xem phân tích nâng cao (không khả dụng với báo cáo công khai).")

    # ════════════════════════════════════════════════════════════
    # TAB 5 — STRATEGY INSIGHTS
    # ════════════════════════════════════════════════════════════
    with tabs[4]:
        insights = A.get("insights", [])
        st.markdown(f'<div class="section-header">💡 Nhận định & đề xuất chiến lược</div>', unsafe_allow_html=True)

        if not insights:
            st.info("Không đủ dữ liệu để tạo nhận định.")
        else:
            for ins in insights:
                css_class = f"insight-{ins['type']}"
                color_map = {"success":T["success"],"warning":T["warning"],"danger":T["danger"],"info":T["accent"]}
                c = color_map.get(ins["type"], T["accent"])
                st.markdown(f"""
                <div class="{css_class}">
                  <div style="display:flex; align-items:flex-start; gap:.8rem;">
                    <span style="font-size:1.4rem;">{ins['icon']}</span>
                    <div>
                      <div style="font-weight:700; color:{T['text']}; margin-bottom:.3rem; font-size:.95rem;">{ins['title']}</div>
                      <div style="color:{T['muted']}; font-size:.88rem; line-height:1.6;">{ins['desc']}</div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div class="section-header">📌 Tóm tắt thông tin ngành</div>', unsafe_allow_html=True)

        col_tags1, col_tags2 = st.columns(2)
        with col_tags1:
            if A.get("industries"):
                pills = " ".join([f'<span class="tag-pill">{s}</span>' for s in A["industries"]])
                st.markdown(f'<div style="margin-bottom:.8rem;"><b style="color:{T["muted"]};font-size:.75rem;font-family:\'JetBrains Mono\',monospace;">NGÀNH</b><br>{pills}</div>', unsafe_allow_html=True)
            if A.get("regions"):
                pills = " ".join([f'<span class="tag-pill">{s}</span>' for s in A["regions"]])
                st.markdown(f'<div><b style="color:{T["muted"]};font-size:.75rem;font-family:\'JetBrains Mono\',monospace;">KHU VỰC</b><br>{pills}</div>', unsafe_allow_html=True)
        with col_tags2:
            if A.get("job_titles"):
                top_jt = A["job_titles"][:12]
                pills = " ".join([f'<span class="tag-pill">{s}</span>' for s in top_jt])
                extra = f'<span style="color:{T["muted"]};font-size:.8rem;"> +{len(A["job_titles"])-12} khác</span>' if len(A["job_titles"])>12 else ""
                st.markdown(f'<div><b style="color:{T["muted"]};font-size:.75rem;font-family:\'JetBrains Mono\',monospace;">VỊ TRÍ CÔNG VIỆC</b><br>{pills}{extra}</div>', unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════
    # TAB 6 — RAW DATA
    # ════════════════════════════════════════════════════════════
    with tabs[5]:
        st.markdown(f'<div class="section-header">📋 Dữ liệu thô</div>', unsafe_allow_html=True)
        if df_raw is not None:
            # Filter controls
            filter_c1, filter_c2, filter_c3 = st.columns(3)
            filtered_df = df_raw.copy()
            with filter_c1:
                if "industry" in df_raw.columns:
                    sel = st.multiselect("Lọc ngành", df_raw["industry"].dropna().unique())
                    if sel: filtered_df = filtered_df[filtered_df["industry"].isin(sel)]
            with filter_c2:
                if "region" in df_raw.columns:
                    sel = st.multiselect("Lọc khu vực", df_raw["region"].dropna().unique())
                    if sel: filtered_df = filtered_df[filtered_df["region"].isin(sel)]
            with filter_c3:
                if "experience_level" in df_raw.columns:
                    sel = st.multiselect("Lọc cấp độ", df_raw["experience_level"].dropna().unique())
                    if sel: filtered_df = filtered_df[filtered_df["experience_level"].isin(sel)]

            st.caption(f"Hiển thị {len(filtered_df):,} / {len(df_raw):,} bản ghi")
            st.dataframe(filtered_df.head(500), use_container_width=True, height=450)

            csv_out = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Tải CSV đã lọc", csv_out, "filtered_data.csv", "text/csv")
        else:
            st.info("📁 Dữ liệu thô không khả dụng với báo cáo công khai. Hãy upload file mới.")
