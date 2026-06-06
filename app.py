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

from i18n import LANGUAGES, TRANSLATIONS, t, tmap

# ─── ENV / SECRETS LOADING ────────────────────────────────────────────────────
def _load_env_file(path=".env"):
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val

_load_env_file(".env")

def get_secret(key: str, section: str = "gdrive", default: str = "") -> str:
    try:
        return st.secrets[section][key]
    except Exception:
        pass
    try:
        return st.secrets[key]
    except Exception:
        pass
    return os.environ.get(key, default)

GDRIVE_FILE_ID    = get_secret("file_id",       section="gdrive") or os.environ.get("GDRIVE_FILE_ID", "")
GDRIVE_LOCAL_FILE = get_secret("local_filename", section="gdrive") or os.environ.get("GDRIVE_LOCAL_FILENAME", "sample_data.csv")

# ─── GOOGLE DRIVE ─────────────────────────────────────────────────────────────
def _gdown_available() -> bool:
    import importlib
    return importlib.util.find_spec("gdown") is not None

def download_sample_from_drive(file_id: str, dest: str, lang: str) -> tuple[bool, str]:
    if not file_id or file_id == "your_google_drive_file_id_here":
        return False, t("drive_err_no_id", lang)
    if not _gdown_available():
        return False, t("drive_err_no_gdown", lang)
    try:
        import gdown
        gdown.download(f"https://drive.google.com/uc?id={file_id}", dest, quiet=True, fuzzy=True)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            return True, f"{t('drive_success', lang)}: `{dest}`"
        return False, t("drive_err_empty", lang)
    except Exception as e:
        return False, f"{t('drive_err_generic', lang)}: {e}"

# ─── COLOR HELPERS ─────────────────────────────────────────────────────────────
def hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c*2 for c in h)
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"

# ─── CONFIG ───────────────────────────────────────────────────────────────────
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
    "🌌 Dark Galaxy": {
        "bg":"#0a0a0f","surface":"#13131a","surface2":"#1c1c28","border":"#2a2a3a",
        "text":"#e8e8f0","muted":"#6b6b85","accent":"#7c6bff","accent2":"#ff6b9d",
        "accent3":"#6bffce","accent4":"#ffb347","success":"#4ade80","warning":"#fbbf24",
        "danger":"#f87171","chart_colors":["#7c6bff","#ff6b9d","#6bffce","#ffb347","#60a5fa","#f472b6","#34d399","#a78bfa"],
        "plotly_template":"plotly_dark",
    },
    "🌊 Ocean Depth": {
        "bg":"#020c18","surface":"#061424","surface2":"#0d2137","border":"#1a3a5c",
        "text":"#cce8ff","muted":"#5a8aaa","accent":"#00d4ff","accent2":"#0066ff",
        "accent3":"#00ffaa","accent4":"#ff8800","success":"#00e676","warning":"#ffab40",
        "danger":"#ff5252","chart_colors":["#00d4ff","#0066ff","#00ffaa","#ff8800","#ff5252","#aa00ff","#64ffda","#40c4ff"],
        "plotly_template":"plotly_dark",
    },
    "🌸 Sakura Light": {
        "bg":"#fff5f7","surface":"#ffffff","surface2":"#fce4ec","border":"#f8bbd0",
        "text":"#3d1a26","muted":"#ad7989","accent":"#e91e8c","accent2":"#ff4081",
        "accent3":"#00bfa5","accent4":"#ff6d00","success":"#00c853","warning":"#ff6d00",
        "danger":"#d50000","chart_colors":["#e91e8c","#ff4081","#00bfa5","#ff6d00","#6200ea","#00b0ff","#69f0ae","#ffab40"],
        "plotly_template":"plotly_white",
    },
    "🍃 Forest Calm": {
        "bg":"#f0f7f0","surface":"#ffffff","surface2":"#e8f5e9","border":"#c8e6c9",
        "text":"#1b3a1f","muted":"#5a8a62","accent":"#2e7d32","accent2":"#00897b",
        "accent3":"#f57f17","accent4":"#1565c0","success":"#43a047","warning":"#fb8c00",
        "danger":"#e53935","chart_colors":["#2e7d32","#00897b","#f57f17","#1565c0","#6a1b9a","#ad1457","#558b2f","#00695c"],
        "plotly_template":"plotly_white",
    },
    "🔥 Cyberpunk": {
        "bg":"#0d0015","surface":"#1a002b","surface2":"#2a0045","border":"#4a0080",
        "text":"#f0e0ff","muted":"#9060c0","accent":"#ff00ff","accent2":"#00ffff",
        "accent3":"#ffff00","accent4":"#ff6600","success":"#00ff88","warning":"#ffff00",
        "danger":"#ff0055","chart_colors":["#ff00ff","#00ffff","#ffff00","#ff6600","#00ff88","#ff0055","#aa00ff","#00aaff"],
        "plotly_template":"plotly_dark",
    },
    "☁️ Cloud White": {
        "bg":"#f8fafc","surface":"#ffffff","surface2":"#f1f5f9","border":"#e2e8f0",
        "text":"#1e293b","muted":"#94a3b8","accent":"#3b82f6","accent2":"#8b5cf6",
        "accent3":"#10b981","accent4":"#f59e0b","success":"#10b981","warning":"#f59e0b",
        "danger":"#ef4444","chart_colors":["#3b82f6","#8b5cf6","#10b981","#f59e0b","#ef4444","#06b6d4","#84cc16","#f97316"],
        "plotly_template":"plotly_white",
    },
}

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if "theme_name" not in st.session_state:
    st.session_state.theme_name = "🌌 Dark Galaxy"
if "lang" not in st.session_state:
    st.session_state.lang = "vi"
if "df" not in st.session_state:
    st.session_state.df = None
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "published" not in st.session_state:
    st.session_state.published = False

T   = THEMES[st.session_state.theme_name]
LNG = st.session_state.lang

# ─── CSS ──────────────────────────────────────────────────────────────────────
def inject_css(t_):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&family=Outfit:wght@300;400;500;600;700&display=swap');
    html,body,[class*="css"]{{font-family:'Outfit',sans-serif!important;color:{t_['text']}!important;}}
    .stApp{{background:{t_['bg']}!important;}}
    #MainMenu,footer,header{{visibility:hidden;}}
    .block-container{{padding-top:1.5rem!important;padding-bottom:3rem!important;max-width:1400px!important;}}
    [data-testid="stSidebar"]{{background:{t_['surface']}!important;border-right:1px solid {t_['border']}!important;}}
    [data-testid="stSidebar"] *{{color:{t_['text']}!important;}}
    [data-testid="stSidebarContent"]{{padding:1.5rem 1rem!important;}}
    .stSelectbox>div>div,.stTextInput>div>div>input,.stTextArea textarea{{background:{t_['surface2']}!important;border:1px solid {t_['border']}!important;color:{t_['text']}!important;border-radius:10px!important;}}
    .stSelectbox [data-baseweb="select"]>div{{background:{t_['surface2']}!important;border-color:{t_['border']}!important;border-radius:10px!important;}}
    [data-testid="stFileUploader"]{{background:{t_['surface']}!important;border:2px dashed {t_['border']}!important;border-radius:16px!important;padding:1rem!important;}}
    [data-testid="stFileUploader"]:hover{{border-color:{t_['accent']}!important;}}
    .stButton>button{{background:{t_['accent']}!important;color:#fff!important;border:none!important;border-radius:10px!important;font-family:'Outfit',sans-serif!important;font-weight:600!important;font-size:.9rem!important;padding:.6rem 1.6rem!important;transition:all .2s!important;box-shadow:0 4px 15px {t_['accent']}44!important;}}
    .stButton>button:hover{{opacity:.88!important;transform:translateY(-1px)!important;}}
    .stTabs [data-baseweb="tab-list"]{{background:{t_['surface']}!important;border-radius:12px!important;padding:.3rem!important;gap:.3rem!important;border:1px solid {t_['border']}!important;}}
    .stTabs [data-baseweb="tab"]{{background:transparent!important;border-radius:8px!important;color:{t_['muted']}!important;font-family:'Outfit',sans-serif!important;font-weight:600!important;padding:.5rem 1.2rem!important;border:none!important;}}
    .stTabs [aria-selected="true"]{{background:{t_['accent']}!important;color:#fff!important;}}
    .stTabs [data-baseweb="tab-panel"]{{background:transparent!important;padding-top:1.5rem!important;}}
    [data-testid="stMetric"]{{background:{t_['surface']}!important;border:1px solid {t_['border']}!important;border-radius:14px!important;padding:1.2rem 1.4rem!important;border-top:3px solid {t_['accent']}!important;}}
    [data-testid="stMetricLabel"]{{color:{t_['muted']}!important;font-family:'JetBrains Mono',monospace!important;font-size:.72rem!important;text-transform:uppercase!important;letter-spacing:.06em!important;}}
    [data-testid="stMetricValue"]{{color:{t_['text']}!important;font-family:'JetBrains Mono',monospace!important;font-size:1.7rem!important;font-weight:700!important;}}
    .streamlit-expanderHeader{{background:{t_['surface']}!important;border:1px solid {t_['border']}!important;border-radius:10px!important;color:{t_['text']}!important;font-weight:600!important;}}
    .streamlit-expanderContent{{background:{t_['surface2']}!important;border:1px solid {t_['border']}!important;border-top:none!important;border-radius:0 0 10px 10px!important;}}
    ::-webkit-scrollbar{{width:6px;height:6px;}}
    ::-webkit-scrollbar-track{{background:{t_['surface']};}}
    ::-webkit-scrollbar-thumb{{background:{t_['border']};border-radius:3px;}}
    ::-webkit-scrollbar-thumb:hover{{background:{t_['accent']};}}
    hr{{border-color:{t_['border']}!important;margin:1.5rem 0!important;}}
    .lens-card{{background:{t_['surface']};border:1px solid {t_['border']};border-radius:16px;padding:1.4rem 1.6rem;margin-bottom:1rem;}}
    .lens-card-accent{{border-top:3px solid {t_['accent']};}}
    .insight-success{{background:{t_['success']}18;border:1px solid {t_['success']}55;border-radius:12px;padding:1rem 1.2rem;margin-bottom:.7rem;}}
    .insight-warning{{background:{t_['warning']}18;border:1px solid {t_['warning']}55;border-radius:12px;padding:1rem 1.2rem;margin-bottom:.7rem;}}
    .insight-danger{{background:{t_['danger']}18;border:1px solid {t_['danger']}55;border-radius:12px;padding:1rem 1.2rem;margin-bottom:.7rem;}}
    .insight-info{{background:{t_['accent']}18;border:1px solid {t_['accent']}55;border-radius:12px;padding:1rem 1.2rem;margin-bottom:.7rem;}}
    .hero-title{{font-family:'Syne',sans-serif;font-weight:800;font-size:clamp(2rem,4vw,3.2rem);line-height:1.1;letter-spacing:-.03em;color:{t_['text']};margin-bottom:.5rem;}}
    .hero-accent{{color:{t_['accent']};}}
    .hero-sub{{font-family:'Outfit',sans-serif;color:{t_['muted']};font-size:1.05rem;line-height:1.7;margin-bottom:1.5rem;}}
    .badge{{display:inline-block;background:{t_['accent']}22;color:{t_['accent']};border:1px solid {t_['accent']}55;border-radius:20px;padding:.25rem .9rem;font-size:.75rem;font-family:'JetBrains Mono',monospace;letter-spacing:.05em;margin-bottom:1rem;}}
    .section-header{{font-family:'Syne',sans-serif;font-weight:700;font-size:1.25rem;color:{t_['text']};margin-bottom:1rem;padding-bottom:.5rem;border-bottom:2px solid {t_['border']};}}
    .tag-pill{{display:inline-block;background:{t_['accent']}22;color:{t_['accent']};border-radius:20px;padding:.2rem .7rem;font-size:.75rem;font-weight:600;margin:.15rem;}}
    .lang-flag{{font-size:1.1rem;cursor:pointer;padding:.2rem .5rem;border-radius:6px;transition:.15s;}}
    .lang-flag:hover{{background:{t_['surface2']};}}
    </style>
    """, unsafe_allow_html=True)

inject_css(T)

# ─── ANALYSIS ENGINE ───────────────────────────────────────────────────────────
def safe_json(d):
    if isinstance(d, dict):  return {k: safe_json(v) for k, v in d.items()}
    if isinstance(d, list):  return [safe_json(i) for i in d]
    if isinstance(d, float) and (np.isnan(d) or np.isinf(d)): return None
    if isinstance(d, np.integer): return int(d)
    if isinstance(d, np.floating): return float(d)
    return d

def analyze(df: pd.DataFrame, lang: str = "vi") -> dict:
    R = {}
    R["total_records"] = len(df)
    R["columns"]    = df.columns.tolist()
    R["industries"] = df["industry"].dropna().unique().tolist() if "industry" in df.columns else []
    R["regions"]    = df["region"].dropna().unique().tolist() if "region" in df.columns else []
    R["job_titles"] = df["job_title"].dropna().unique().tolist() if "job_title" in df.columns else []

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"]).sort_values("date")
        df["_period"] = df["date"].dt.to_period("M")

    # Trends
    trends = {}
    for col, agg in [("job_openings","sum"),("avg_salary","mean"),("growth_score","mean")]:
        if col in df.columns and "date" in df.columns:
            g = df.groupby("_period")[col].agg(agg).reset_index()
            g["date"] = g["_period"].dt.to_timestamp()
            if len(g) >= 3 and col == "job_openings":
                X = ((g["date"]-g["date"].min()).dt.days).values.reshape(-1,1)
                m = LinearRegression().fit(X, g[col].values)
                trends["job_openings_slope"] = round(float(m.coef_[0]),4)
                trends["job_openings_trend"] = t("trend_increasing", lang) if m.coef_[0]>0 else t("trend_decreasing", lang)
            trends[f"{col}_monthly"] = {
                "labels":[str(d.date()) for d in g["date"]],
                "values":[round(float(v),2) for v in g[col]]
            }
    R["trends"] = trends

    # Forecast
    forecast = {}
    if "job_openings" in df.columns and "date" in df.columns:
        g = df.groupby("_period")["job_openings"].sum().reset_index()
        g["date"] = g["_period"].dt.to_timestamp()
        if len(g) >= 4:
            ts = (g["date"]-g["date"].min()).dt.days.values.reshape(-1,1)
            poly = PolynomialFeatures(degree=2)
            Xp = poly.fit_transform(ts)
            ridge = Ridge(alpha=1.0).fit(Xp, g["job_openings"].values)
            last_ts = float(ts.max()); last_dt = g["date"].max()
            f_days  = np.array([last_ts+30*i for i in range(1,7)]).reshape(-1,1)
            f_preds = ridge.predict(poly.transform(f_days))
            forecast["job_openings"] = {
                "labels":[str((last_dt+pd.DateOffset(months=i)).date()) for i in range(1,7)],
                "values":[max(0,round(float(v),0)) for v in f_preds]
            }

    if "avg_salary" in df.columns and "salary_growth_rate" in df.columns:
        gr = float(df["salary_growth_rate"].mean())
        cs = float(df["avg_salary"].mean())
        forecast["salary"] = {
            "labels":[f"{t('forecast_col_month', lang)} +{i}" for i in range(1,7)],
            "values":[round(cs*(1+gr/100)**i,2) for i in range(1,7)]
        }

    if "growth_score" in df.columns:
        gs = float(df["growth_score"].mean())
        if gs > 60:
            outlook = t("outlook_positive", lang)
        elif gs > 40:
            outlook = t("outlook_neutral", lang)
        else:
            outlook = t("outlook_caution", lang)
        forecast["growth_score"] = {
            "mean":round(gs,2),
            "std":round(float(df["growth_score"].std()),2),
            "outlook": outlook
        }
    R["forecast"] = forecast

    # Distributions
    dists = {}
    for col in ["experience_level","competition_level","automation_risk","demand_forecast"]:
        if col in df.columns:
            vc = df[col].value_counts()
            dists[col] = {"labels":vc.index.tolist(),"values":vc.values.tolist()}

    if "remote_ratio" in df.columns:
        bins=[0,20,40,60,80,100]; labels=["0–20%","21–40%","41–60%","61–80%","81–100%"]
        counts=pd.cut(df["remote_ratio"],bins=bins,labels=labels).value_counts().reindex(labels).fillna(0)
        dists["remote_ratio"]={"mean":round(float(df["remote_ratio"].mean()),1),"bins":labels,"values":counts.astype(int).tolist()}

    if "job_title" in df.columns and "avg_salary" in df.columns:
        tj=df.groupby("job_title")["avg_salary"].mean().nlargest(8)
        dists["top_paying_jobs"]={"labels":tj.index.tolist(),"values":[round(float(v),2) for v in tj.values]}

    if "region" in df.columns and "job_openings" in df.columns:
        rj=df.groupby("region")["job_openings"].sum().nlargest(8)
        dists["jobs_by_region"]={"labels":rj.index.tolist(),"values":[int(v) for v in rj.values]}

    if "required_skills" in df.columns:
        sk=df["required_skills"].dropna().str.split(",").explode().str.strip().value_counts().head(12)
        dists["top_skills"]={"labels":sk.index.tolist(),"values":sk.values.tolist()}

    R["distributions"] = dists

    # KPIs
    R["kpis"] = {
        "avg_salary":        round(float(df["avg_salary"].mean()),2) if "avg_salary" in df.columns else None,
        "total_openings":    int(df["job_openings"].sum()) if "job_openings" in df.columns else None,
        "avg_growth_score":  round(float(df["growth_score"].mean()),1) if "growth_score" in df.columns else None,
        "avg_salary_growth": round(float(df["salary_growth_rate"].mean()),2) if "salary_growth_rate" in df.columns else None,
        "avg_remote":        round(float(df["remote_ratio"].mean()),1) if "remote_ratio" in df.columns else None,
        "industry":          df["industry"].mode()[0] if "industry" in df.columns and len(df)>0 else "N/A",
    }

    # Insights
    insights = []
    if "automation_risk" in df.columns and df["automation_risk"].dtype==object:
        hr=(df["automation_risk"].str.lower()=="high").mean()*100
        if hr>40:
            insights.append({"type":"warning","icon":"⚠️","title":t("insight_auto_high_title",lang),"desc":f"{hr:.0f}{t('insight_auto_high_desc',lang)}"})
        else:
            insights.append({"type":"success","icon":"🛡️","title":t("insight_auto_low_title",lang),"desc":t("insight_auto_low_desc",lang).replace("%",f"{hr:.0f}%",1)})

    if "remote_ratio" in df.columns:
        ar=df["remote_ratio"].mean()
        if ar>60:
            insights.append({"type":"info","icon":"🌐","title":t("insight_remote_high_title",lang),"desc":t("insight_remote_high_desc",lang).replace("%",f"{ar:.0f}%",1)})
        elif ar<25:
            insights.append({"type":"info","icon":"🏢","title":t("insight_remote_low_title",lang),"desc":t("insight_remote_low_desc",lang).replace("%",f"{ar:.0f}%",1)})

    if "growth_score" in df.columns:
        gs=df["growth_score"].mean()
        if gs>65:
            insights.append({"type":"success","icon":"🚀","title":t("insight_growth_high_title",lang),"desc":t("insight_growth_high_desc",lang).replace("/100",f"{gs:.1f}/100",1)})
        elif gs<40:
            insights.append({"type":"danger","icon":"📉","title":t("insight_growth_low_title",lang),"desc":t("insight_growth_low_desc",lang).replace("/100",f"{gs:.1f}/100",1)})

    if "salary_growth_rate" in df.columns:
        sgr=df["salary_growth_rate"].mean()
        if sgr>8:
            insights.append({"type":"success","icon":"💰","title":t("insight_sal_exc_title",lang),"desc":t("insight_sal_exc_desc",lang).replace("%/",f"{sgr:.1f}%/",1)})
        elif sgr>4:
            insights.append({"type":"info","icon":"💵","title":t("insight_sal_ok_title",lang),"desc":t("insight_sal_ok_desc",lang).replace("%/",f"{sgr:.1f}%/",1)})

    if "competition_level" in df.columns and df["competition_level"].dtype==object:
        hc=(df["competition_level"].str.lower()=="high").mean()*100
        if hc>50:
            insights.append({"type":"warning","icon":"⚔️","title":t("insight_comp_high_title",lang),"desc":t("insight_comp_high_desc",lang).replace("%",f"{hc:.0f}%",1)})

    R["insights"] = insights
    return safe_json(R)

# ─── PLOTLY HELPERS ────────────────────────────────────────────────────────────
def pgo(title=""):
    return dict(
        template=T["plotly_template"],
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Outfit,sans-serif",color=T["text"],size=12),
        title=dict(text=title,font=dict(family="Syne,sans-serif",size=15,color=T["text"]),x=0,pad=dict(l=0)),
        margin=dict(l=10,r=10,t=40 if title else 10,b=10),
        colorway=T["chart_colors"],
        legend=dict(font=dict(color=T["muted"],size=11)),
        xaxis=dict(gridcolor=T["border"],tickfont=dict(color=T["muted"]),linecolor=T["border"]),
        yaxis=dict(gridcolor=T["border"],tickfont=dict(color=T["muted"]),linecolor=T["border"]),
    )

def fmt_num(n, pre=""):
    if n is None: return "N/A"
    if n>=1e9: return f"{pre}{n/1e9:.1f}B"
    if n>=1e6: return f"{pre}{n/1e6:.1f}M"
    if n>=1e3: return f"{pre}{n/1e3:.1f}K"
    return f"{pre}{n:,.0f}"

def chart_line(labels, values, title, color=None):
    color = color or T["accent"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=labels, y=values, mode="lines+markers",
        line=dict(color=color,width=2.5),
        marker=dict(color=color,size=6),
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
            marker=dict(color=T["chart_colors"][:len(labels)],line=dict(width=0)),
            hovertemplate="%{y}<br><b>%{x:,.0f}</b><extra></extra>"
        ))
        fig.update_layout(**{**pgo(title),"yaxis":dict(gridcolor=T["border"],tickfont=dict(color=T["muted"],size=11),autorange="reversed")})
    else:
        fig = go.Figure(go.Bar(
            x=labels, y=values,
            marker=dict(color=color,opacity=.85,line=dict(width=0)),
            hovertemplate="%{x}<br><b>%{y:,.0f}</b><extra></extra>"
        ))
        fig.update_layout(**pgo(title))
    return fig

def chart_donut(labels, values, title):
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=.55,
        marker=dict(colors=T["chart_colors"][:len(labels)],line=dict(color=T["bg"],width=2)),
        textfont=dict(color=T["text"],size=12),
        hovertemplate="%{label}<br><b>%{value}</b> (%{percent})<extra></extra>"
    ))
    fig.update_layout(**{**pgo(title),"showlegend":True,
        "legend":dict(font=dict(color=T["muted"],size=11),orientation="v",x=1.02)})
    return fig

def chart_scatter(df, lang):
    if "avg_salary" not in df.columns or "growth_score" not in df.columns: return None
    color_col = "experience_level" if "experience_level" in df.columns else None
    fig = px.scatter(
        df.sample(min(500,len(df))),
        x="avg_salary", y="growth_score",
        color=color_col,
        size="job_openings" if "job_openings" in df.columns else None,
        hover_data=[c for c in ["job_title","region","industry"] if c in df.columns],
        color_discrete_sequence=T["chart_colors"],
        labels={"avg_salary":t("scatter_x_label",lang),"growth_score":t("scatter_y_label",lang)},
    )
    fig.update_layout(**pgo(t("chart_scatter",lang)))
    return fig

def chart_heatmap(df, lang):
    num_cols=[c for c in ["avg_salary","job_openings","growth_score","salary_growth_rate","remote_ratio"] if c in df.columns]
    if len(num_cols)<2: return None
    corr=df[num_cols].corr()
    labels_map = tmap("heatmap_labels", lang)
    fig=go.Figure(go.Heatmap(
        z=corr.values,
        x=[labels_map.get(c,c) for c in corr.columns],
        y=[labels_map.get(c,c) for c in corr.index],
        colorscale=[[0,T["danger"]],[0.5,T["surface2"]],[1,T["accent"]]],
        text=np.round(corr.values,2), texttemplate="%{text}",
        hovertemplate="%{y} × %{x}<br>r = %{z:.3f}<extra></extra>",
        zmin=-1, zmax=1,
    ))
    fig.update_layout(**pgo(t("chart_corr_heatmap",lang)))
    return fig

def chart_salary_dist(df, lang):
    if "avg_salary" not in df.columns: return None
    if "experience_level" in df.columns:
        fig=go.Figure()
        for i,lvl in enumerate(df["experience_level"].dropna().unique()):
            vals=df[df["experience_level"]==lvl]["avg_salary"]
            fig.add_trace(go.Box(
                x=[lvl]*len(vals), y=vals, name=str(lvl),
                marker_color=T["chart_colors"][i%len(T["chart_colors"])],
                boxmean=True,
                hovertemplate=f"<b>{lvl}</b><br>%{{y:,.0f}}<extra></extra>"
            ))
        fig.update_layout(**pgo(t("chart_salary_dist",lang)))
    else:
        fig=px.histogram(df,x="avg_salary",nbins=30,
            color_discrete_sequence=[T["accent"]],title=t("chart_salary_hist",lang))
        fig.update_layout(**pgo(t("chart_salary_hist",lang)))
    return fig

def chart_timeline_multi(A, lang):
    tr=A.get("trends",{})
    if "job_openings_monthly" not in tr or "growth_score_monthly" not in tr: return None
    fig=make_subplots(specs=[[{"secondary_y":True}]])
    jd=tr["job_openings_monthly"]; gs=tr["growth_score_monthly"]
    fig.add_trace(go.Bar(x=jd["labels"],y=jd["values"],name=t("chart_jobs_monthly",lang),
        marker_color=hex_to_rgba(T["accent"],0.73),
        hovertemplate="%{x}<br><b>%{y:,.0f}</b><extra></extra>"),secondary_y=False)
    fig.add_trace(go.Scatter(x=gs["labels"],y=gs["values"],name=t("chart_growth_monthly",lang),
        line=dict(color=T["accent2"],width=2.5),mode="lines+markers",
        marker=dict(size=5),hovertemplate="%{x}<br><b>%{y:.1f}</b><extra></extra>"),secondary_y=True)
    opts=pgo(t("chart_dual_axis",lang))
    opts["yaxis2"]=dict(gridcolor="rgba(0,0,0,0)",tickfont=dict(color=T["muted"]),title="Score")
    opts["legend"]=dict(orientation="h",y=-0.15,font=dict(color=T["muted"],size=11))
    fig.update_layout(**opts)
    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # ── Logo ──
    st.markdown(f"""
    <div style="text-align:center;padding:.5rem 0 1rem;">
      <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.5rem;color:{T['text']};">
        Industry<span style="color:{T['accent']}">Lens</span>
      </div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:.65rem;color:{T['muted']};margin-top:.3rem;">
        {t('app_subtitle', LNG)}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Language selector ──
    st.markdown(f'<div class="section-header">{t("sidebar_language", LNG)}</div>', unsafe_allow_html=True)
    lang_labels = [v["label"] for v in LANGUAGES.values()]
    lang_codes  = list(LANGUAGES.keys())
    cur_idx     = lang_codes.index(LNG) if LNG in lang_codes else 0
    new_lang_label = st.selectbox("lang_sel", lang_labels, index=cur_idx, label_visibility="collapsed")
    new_lang_code  = lang_codes[lang_labels.index(new_lang_label)]
    if new_lang_code != LNG:
        st.session_state.lang = new_lang_code
        st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Theme selector ──
    st.markdown(f'<div class="section-header">{t("sidebar_theme", LNG)}</div>', unsafe_allow_html=True)
    new_theme = st.selectbox("theme", list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.theme_name),
        label_visibility="collapsed")
    if new_theme != st.session_state.theme_name:
        st.session_state.theme_name = new_theme
        st.rerun()

    cols_p = st.columns(4)
    for i,(lbl_key,color) in enumerate(zip(
        ["color_main","color_sub1","color_sub2","color_sub3"],
        [T["accent"],T["accent2"],T["accent3"],T["accent4"]]
    )):
        cols_p[i].markdown(f"""
        <div style="text-align:center;">
          <div style="width:26px;height:26px;border-radius:50%;background:{color};margin:0 auto 3px;border:2px solid {T['border']};"></div>
          <div style="font-size:.58rem;color:{T['muted']};">{t(lbl_key,LNG)}</div>
        </div>""", unsafe_allow_html=True)

    with st.expander(t("sidebar_custom_color", LNG)):
        custom_accent = st.color_picker(t("sidebar_color_label", LNG), T["accent"])
        if custom_accent != T["accent"]:
            THEMES[st.session_state.theme_name]["accent"] = custom_accent
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Google Drive ──
    st.markdown(f'<div class="section-header">{t("sidebar_gdrive", LNG)}</div>', unsafe_allow_html=True)
    gdrive_ok = bool(GDRIVE_FILE_ID and GDRIVE_FILE_ID != "your_google_drive_file_id_here")

    if gdrive_ok:
        file_exists = os.path.exists(GDRIVE_LOCAL_FILE)
        if file_exists:
            fsize = os.path.getsize(GDRIVE_LOCAL_FILE)/1024
            st.markdown(f"""
            <div style="background:{T['success']}18;border:1px solid {T['success']}55;border-radius:10px;padding:.7rem 1rem;font-size:.82rem;margin-bottom:.6rem;">
              ✅ <b>{GDRIVE_LOCAL_FILE}</b><br>
              <span style="color:{T['muted']};">{fsize:.1f} KB · {t('drive_downloaded',LNG)}</span>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:{T['warning']}18;border:1px solid {T['warning']}55;border-radius:10px;padding:.7rem 1rem;font-size:.82rem;margin-bottom:.6rem;">
              {t('drive_not_downloaded',LNG)}
            </div>""", unsafe_allow_html=True)

        c1,c2 = st.columns(2)
        with c1:
            if st.button(t("drive_btn_download",LNG), use_container_width=True, key="btn_dl"):
                with st.spinner(t("drive_downloading",LNG)):
                    ok,msg = download_sample_from_drive(GDRIVE_FILE_ID, GDRIVE_LOCAL_FILE, LNG)
                (st.success if ok else st.error)(msg)
                if ok: st.rerun()
        with c2:
            if file_exists and st.button(t("drive_btn_refresh",LNG), use_container_width=True, key="btn_rf"):
                with st.spinner(t("drive_updating",LNG)):
                    ok,msg = download_sample_from_drive(GDRIVE_FILE_ID, GDRIVE_LOCAL_FILE, LNG)
                (st.success if ok else st.error)(msg)
                if ok: st.rerun()

        if file_exists:
            if st.button(t("drive_btn_use",LNG), use_container_width=True, key="btn_use"):
                with st.spinner(t("drive_analyzing",LNG)):
                    try:
                        df_ = pd.read_csv(GDRIVE_LOCAL_FILE)
                        st.session_state.df = df_
                        st.session_state.analysis = analyze(df_, LNG)
                        st.session_state.analysis["uploader"] = "Drive Sample"
                        st.session_state.analysis["uploaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        st.session_state.published = False
                        st.success(f"✅ {len(df_):,} {t('drive_records_loaded',LNG)}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ {e}")
    else:
        st.markdown(f"""
        <div style="background:{T['surface2']};border:1px solid {T['border']};border-radius:10px;padding:.8rem 1rem;font-size:.8rem;color:{T['muted']};">
          {t('drive_not_configured',LNG)}
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── File upload ──
    st.markdown(f'<div class="section-header">{t("sidebar_upload", LNG)}</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("upload", type=["csv","xlsx","xls"], label_visibility="collapsed")
    uploader_name = st.text_input(t("upload_name_label",LNG),
        placeholder=t("upload_placeholder",LNG), label_visibility="visible")

    if uploaded:
        if st.button(t("upload_btn",LNG), use_container_width=True):
            with st.spinner(t("upload_spinner",LNG)):
                try:
                    df_ = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
                    st.session_state.df = df_
                    st.session_state.analysis = analyze(df_, LNG)
                    st.session_state.analysis["uploader"] = uploader_name or t("upload_placeholder",LNG)
                    st.session_state.analysis["uploaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    st.session_state.published = False
                    st.success(f"{t('upload_success',LNG)} {len(df_):,} {t('upload_records',LNG)}")
                except Exception as e:
                    st.error(f"{t('upload_error',LNG)}: {e}")

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Public reports ──
    public_files = []
    for f in os.listdir(PUBLIC_DIR):
        if f.endswith(".json"):
            try:
                with open(os.path.join(PUBLIC_DIR,f)) as fp:
                    meta = json.load(fp)
                public_files.append({"id":f.replace(".json",""),**meta.get("kpis",{}),
                    "total_records":meta.get("total_records",0),
                    "uploader":meta.get("uploader",""),
                    "uploaded_at":meta.get("uploaded_at","")})
            except: pass

    if public_files:
        st.markdown(f'<div class="section-header">{t("sidebar_public",LNG)} ({len(public_files)})</div>', unsafe_allow_html=True)
        placeholder = t("public_select_placeholder", LNG)
        opts = [placeholder] + [f"{p.get('industry','?')} · {p['uploader']} · {p['uploaded_at']}" for p in public_files]
        sel = st.selectbox("pub", opts, label_visibility="collapsed")
        if sel != placeholder:
            idx = opts.index(sel) - 1
            try:
                with open(os.path.join(PUBLIC_DIR, public_files[idx]["id"]+".json"), encoding="utf-8") as fp:
                    st.session_state.analysis = json.load(fp)
                    st.session_state.df = None
                    st.success(t("public_loaded",LNG))
            except: pass

    # Columns hint
    st.markdown(f"""
    <div style="margin-top:1.5rem;padding:.8rem;background:{T['surface2']};border-radius:10px;border:1px solid {T['border']};">
      <div style="font-family:'JetBrains Mono',monospace;font-size:.62rem;color:{T['muted']};line-height:1.9;">
        {t('sidebar_columns_hint',LNG)}:<br>
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

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════════════════════════
A      = st.session_state.analysis
df_raw = st.session_state.df

if A is None:
    # ── Hero landing ──
    st.markdown(f"""
    <div style="max-width:800px;margin:4rem auto 0;text-align:center;">
      <div class="badge">{t('app_badge',LNG)}</div>
      <div class="hero-title">
        {t('hero_title_line1',LNG)}<br>
        <span class="hero-accent">{t('hero_title_line2',LNG)}</span>
      </div>
      <p class="hero-sub">{t('hero_sub',LNG)}</p>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    for col,(ik,tk,dk) in zip([c1,c2,c3],[
        ("📈","feat_trend_title","feat_trend_desc"),
        ("🔮","feat_forecast_title","feat_forecast_desc"),
        ("💡","feat_strategy_title","feat_strategy_desc"),
    ]):
        col.markdown(f"""
        <div class="lens-card lens-card-accent" style="text-align:center;padding:2rem 1.5rem;">
          <div style="font-size:2.2rem;margin-bottom:.8rem;">{ik}</div>
          <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;color:{T['text']};margin-bottom:.5rem;">{t(tk,LNG)}</div>
          <div style="font-size:.85rem;color:{T['muted']};line-height:1.6;">{t(dk,LNG)}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center;margin-top:3rem;color:{T['muted']};font-size:.9rem;">
      {t('hero_cta',LNG)}
    </div>""", unsafe_allow_html=True)

else:
    # ── Dashboard header ──
    kpis = A.get("kpis",{})
    h1,h2 = st.columns([1,1])
    with h1:
        st.markdown(f"""
        <div style="padding:.5rem 0;">
          <div class="badge">📊 {kpis.get('industry','N/A')} · {A.get('total_records',0):,} {t('dashboard_records',LNG)}</div>
          <div class="hero-title" style="font-size:2rem;">{t('dashboard_title',LNG)}</div>
          <div style="font-size:.85rem;color:{T['muted']};">
            👤 {A.get('uploader','—')} &nbsp;·&nbsp; 🕒 {A.get('uploaded_at','—')}
          </div>
        </div>""", unsafe_allow_html=True)
    with h2:
        bc1,bc2 = st.columns(2)
        with bc1:
            if not st.session_state.published:
                if st.button(t("btn_share_public",LNG), use_container_width=True):
                    fid = str(uuid.uuid4())[:8]
                    with open(os.path.join(PUBLIC_DIR,f"{fid}.json"),"w",encoding="utf-8") as fp:
                        json.dump(A, fp, ensure_ascii=False, indent=2)
                    st.session_state.published = True
                    st.success(f"{t('published_success',LNG)} `{fid}`")
            else:
                st.success(t("btn_already_public",LNG))
        with bc2:
            st.download_button(t("btn_download_json",LNG),
                json.dumps(A,ensure_ascii=False,indent=2), "report.json","application/json",
                use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── KPIs ──
    k1,k2,k3,k4,k5 = st.columns(5)
    with k1: st.metric(t("kpi_salary",LNG),    fmt_num(kpis.get("avg_salary"),"$"))
    with k2: st.metric(t("kpi_openings",LNG),  fmt_num(kpis.get("total_openings")))
    with k3: st.metric(t("kpi_growth",LNG),    f"{kpis.get('avg_growth_score','—')}/100")
    with k4: st.metric(t("kpi_salary_growth",LNG), f"{kpis.get('avg_salary_growth','—')}%")
    with k5: st.metric(t("kpi_remote",LNG),    f"{kpis.get('avg_remote','—')}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TABS ──
    tab_labels = [t(k,LNG) for k in ["tab_trends","tab_forecast","tab_distribution","tab_advanced","tab_strategy","tab_data"]]
    tabs = st.tabs(tab_labels)

    # ── TAB 1: TRENDS ──────────────────────────────────────────────────────────
    with tabs[0]:
        trends = A.get("trends",{})
        st.markdown(f'<div class="section-header">{t("trends_header",LNG)}</div>', unsafe_allow_html=True)

        if trends.get("job_openings_trend"):
            direction = trends["job_openings_trend"]
            up = direction == t("trend_increasing",LNG)
            color_b = T["success"] if up else T["danger"]
            icon_b  = "📈" if up else "📉"
            st.markdown(f"""
            <div style="background:{color_b}18;border:1px solid {color_b}55;border-radius:10px;padding:.8rem 1.2rem;margin-bottom:1.2rem;display:inline-block;">
              {icon_b} {t('trend_direction_msg',LNG)} <b style="color:{color_b};">{direction}</b>
              &nbsp;({t('trend_coefficient',LNG)}: {trends.get('job_openings_slope',0):+.2f} {t('trend_unit',LNG)})
            </div>""", unsafe_allow_html=True)

        r1c1,r1c2 = st.columns(2)
        with r1c1:
            if "job_openings_monthly" in trends:
                d = trends["job_openings_monthly"]
                st.plotly_chart(chart_line(d["labels"],d["values"],t("chart_jobs_monthly",LNG),T["accent"]), use_container_width=True)
            else:
                st.info(t("no_jobs_date",LNG))
        with r1c2:
            if "avg_salary_monthly" in trends:
                d = trends["avg_salary_monthly"]
                st.plotly_chart(chart_line(d["labels"],d["values"],t("chart_salary_monthly",LNG),T["accent2"]), use_container_width=True)
            else:
                st.info(t("no_salary_date",LNG))

        r2c1,r2c2 = st.columns(2)
        with r2c1:
            if "growth_score_monthly" in trends:
                d = trends["growth_score_monthly"]
                st.plotly_chart(chart_line(d["labels"],d["values"],t("chart_growth_monthly",LNG),T["accent3"]), use_container_width=True)
        with r2c2:
            fig_dual = chart_timeline_multi(A, LNG)
            if fig_dual:
                st.plotly_chart(fig_dual, use_container_width=True)

    # ── TAB 2: FORECAST ────────────────────────────────────────────────────────
    with tabs[1]:
        fc = A.get("forecast",{})
        st.markdown(f'<div class="section-header">{t("forecast_header",LNG)}</div>', unsafe_allow_html=True)

        if "growth_score" in fc:
            gs = fc["growth_score"]
            outlook_str = gs["outlook"]
            is_pos = t("outlook_positive","vi")[:3] in outlook_str or "Positive" in outlook_str or "好調" in outlook_str or "긍정" in outlook_str
            is_neu = t("outlook_neutral","vi")[:4] in outlook_str or "Neutral" in outlook_str or "普通" in outlook_str or "보통" in outlook_str
            color_gs = T["success"] if is_pos else (T["warning"] if is_neu else T["danger"])
            st.markdown(f"""
            <div style="background:{T['surface']};border:1px solid {T['border']};border-radius:16px;padding:1.8rem 2rem;margin-bottom:1.5rem;display:flex;align-items:center;gap:2rem;flex-wrap:wrap;">
              <div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:.7rem;color:{T['muted']};text-transform:uppercase;letter-spacing:.08em;">{t('forecast_avg_growth',LNG)}</div>
                <div style="font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;color:{T['text']};">{gs['mean']}<span style="font-size:1.2rem;color:{T['muted']};">/100</span></div>
                <div style="font-size:.85rem;color:{T['muted']};">{t('forecast_std_dev',LNG)}: ±{gs['std']}</div>
              </div>
              <div style="background:{color_gs}22;border:1px solid {color_gs}55;border-radius:12px;padding:.8rem 1.5rem;">
                <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.1rem;color:{color_gs};">{t('forecast_outlook',LNG)}: {gs['outlook']}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        fc1,fc2 = st.columns(2)
        with fc1:
            if "job_openings" in fc:
                d = fc["job_openings"]
                st.plotly_chart(chart_bar(d["labels"],d["values"],t("chart_forecast_jobs",LNG),T["accent4"]), use_container_width=True)
                st.dataframe(pd.DataFrame({
                    t("forecast_col_month",LNG): d["labels"],
                    t("forecast_col_openings",LNG): [int(v) for v in d["values"]]
                }), use_container_width=True, hide_index=True)
            else:
                st.info(t("no_forecast_jobs",LNG))
        with fc2:
            if "salary" in fc:
                d = fc["salary"]
                st.plotly_chart(chart_line(d["labels"],d["values"],t("chart_forecast_salary",LNG),T["accent2"]), use_container_width=True)
                st.dataframe(pd.DataFrame({
                    t("forecast_col_month",LNG): d["labels"],
                    t("forecast_col_salary",LNG): [f"${v:,.0f}" for v in d["values"]]
                }), use_container_width=True, hide_index=True)
            else:
                st.info(t("no_forecast_salary",LNG))

    # ── TAB 3: DISTRIBUTION ────────────────────────────────────────────────────
    with tabs[2]:
        dist = A.get("distributions",{})
        st.markdown(f'<div class="section-header">{t("dist_header",LNG)}</div>', unsafe_allow_html=True)

        d1,d2,d3 = st.columns(3)
        with d1:
            if "experience_level" in dist:
                d=dist["experience_level"]
                st.plotly_chart(chart_donut(d["labels"],d["values"],t("chart_exp_level",LNG)), use_container_width=True)
        with d2:
            if "competition_level" in dist:
                d=dist["competition_level"]
                st.plotly_chart(chart_donut(d["labels"],d["values"],t("chart_competition",LNG)), use_container_width=True)
        with d3:
            if "automation_risk" in dist:
                d=dist["automation_risk"]
                st.plotly_chart(chart_donut(d["labels"],d["values"],t("chart_auto_risk",LNG)), use_container_width=True)

        d4,d5 = st.columns(2)
        with d4:
            if "top_paying_jobs" in dist:
                d=dist["top_paying_jobs"]
                st.plotly_chart(chart_bar(d["labels"],d["values"],t("chart_top_jobs",LNG),horizontal=True), use_container_width=True)
        with d5:
            if "top_skills" in dist:
                d=dist["top_skills"]
                st.plotly_chart(chart_bar(d["labels"],d["values"],t("chart_top_skills",LNG),horizontal=True), use_container_width=True)

        d6,d7 = st.columns(2)
        with d6:
            if "jobs_by_region" in dist:
                d=dist["jobs_by_region"]
                st.plotly_chart(chart_bar(d["labels"],d["values"],t("chart_jobs_region",LNG),T["accent3"]), use_container_width=True)
        with d7:
            if "demand_forecast" in dist:
                d=dist["demand_forecast"]
                st.plotly_chart(chart_donut(d["labels"],d["values"],t("chart_demand_dist",LNG)), use_container_width=True)

        if "remote_ratio" in dist:
            rd=dist["remote_ratio"]
            st.markdown(f"""
            <div class="lens-card" style="margin-bottom:1rem;">
              <span style="font-family:'JetBrains Mono',monospace;font-size:.7rem;color:{T['muted']};">{t('remote_avg_label',LNG)}</span>
              <span style="font-size:1.6rem;font-weight:700;font-family:'JetBrains Mono',monospace;margin-left:1rem;">{rd['mean']}%</span>
            </div>""", unsafe_allow_html=True)
            st.plotly_chart(chart_bar(rd["bins"],rd["values"],t("chart_remote_dist",LNG),T["accent2"]), use_container_width=True)

    # ── TAB 4: ADVANCED ────────────────────────────────────────────────────────
    with tabs[3]:
        st.markdown(f'<div class="section-header">{t("advanced_header",LNG)}</div>', unsafe_allow_html=True)
        if df_raw is not None:
            a1,a2 = st.columns(2)
            with a1:
                fig_s = chart_scatter(df_raw, LNG)
                st.plotly_chart(fig_s, use_container_width=True) if fig_s else st.info(t("no_scatter",LNG))
            with a2:
                fig_b = chart_salary_dist(df_raw, LNG)
                st.plotly_chart(fig_b, use_container_width=True) if fig_b else st.info(t("no_salary_col",LNG))

            fig_h = chart_heatmap(df_raw, LNG)
            if fig_h:
                st.plotly_chart(fig_h, use_container_width=True)

            if "region" in df_raw.columns and "avg_salary" in df_raw.columns:
                rs = df_raw.groupby("region")["avg_salary"].mean().reset_index().sort_values("avg_salary",ascending=False)
                fig_rs = px.bar(rs, x="region", y="avg_salary",
                    color="avg_salary",
                    color_continuous_scale=[[0,hex_to_rgba(T["accent"],0.4)],[1,T["accent"]]],
                    labels={"region":t("salary_region_x",LNG),"avg_salary":t("salary_region_y",LNG)},
                    title=t("chart_salary_region",LNG))
                fig_rs.update_layout(**pgo())
                fig_rs.update_coloraxes(showscale=False)
                st.plotly_chart(fig_rs, use_container_width=True)

            if "date" in df_raw.columns and "salary_growth_rate" in df_raw.columns:
                df_tmp = df_raw.copy()
                df_tmp["date"] = pd.to_datetime(df_tmp["date"], errors="coerce")
                df_tmp = df_tmp.dropna(subset=["date"])
                g = df_tmp.groupby(df_tmp["date"].dt.to_period("M"))["salary_growth_rate"].mean().reset_index()
                g["date"] = g["date"].dt.to_timestamp()
                st.plotly_chart(chart_line(
                    [str(d.date()) for d in g["date"]], g["salary_growth_rate"].tolist(),
                    t("chart_salary_growth_t",LNG), T["accent4"]
                ), use_container_width=True)
        else:
            st.info(t("no_advanced_raw",LNG))

    # ── TAB 5: STRATEGY ────────────────────────────────────────────────────────
    with tabs[4]:
        insights = A.get("insights",[])
        st.markdown(f'<div class="section-header">{t("strategy_header",LNG)}</div>', unsafe_allow_html=True)

        if not insights:
            st.info(t("no_insights",LNG))
        else:
            for ins in insights:
                color_map = {"success":T["success"],"warning":T["warning"],"danger":T["danger"],"info":T["accent"]}
                c_ = color_map.get(ins["type"], T["accent"])
                st.markdown(f"""
                <div class="insight-{ins['type']}">
                  <div style="display:flex;align-items:flex-start;gap:.8rem;">
                    <span style="font-size:1.4rem;">{ins['icon']}</span>
                    <div>
                      <div style="font-weight:700;color:{T['text']};margin-bottom:.3rem;font-size:.95rem;">{ins['title']}</div>
                      <div style="color:{T['muted']};font-size:.88rem;line-height:1.6;">{ins['desc']}</div>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div class="section-header">{t("summary_header",LNG)}</div>', unsafe_allow_html=True)

        sc1,sc2 = st.columns(2)
        with sc1:
            if A.get("industries"):
                pills=" ".join([f'<span class="tag-pill">{s}</span>' for s in A["industries"]])
                st.markdown(f'<div style="margin-bottom:.8rem;"><b style="color:{T["muted"]};font-size:.75rem;font-family:\'JetBrains Mono\',monospace;">{t("tag_industry",LNG)}</b><br>{pills}</div>', unsafe_allow_html=True)
            if A.get("regions"):
                pills=" ".join([f'<span class="tag-pill">{s}</span>' for s in A["regions"]])
                st.markdown(f'<div><b style="color:{T["muted"]};font-size:.75rem;font-family:\'JetBrains Mono\',monospace;">{t("tag_region",LNG)}</b><br>{pills}</div>', unsafe_allow_html=True)
        with sc2:
            if A.get("job_titles"):
                top_jt = A["job_titles"][:12]
                pills  = " ".join([f'<span class="tag-pill">{s}</span>' for s in top_jt])
                extra  = f'<span style="color:{T["muted"]};font-size:.8rem;"> +{len(A["job_titles"])-12} {t("tag_others",LNG)}</span>' if len(A["job_titles"])>12 else ""
                st.markdown(f'<div><b style="color:{T["muted"]};font-size:.75rem;font-family:\'JetBrains Mono\',monospace;">{t("tag_job_title",LNG)}</b><br>{pills}{extra}</div>', unsafe_allow_html=True)

    # ── TAB 6: RAW DATA ────────────────────────────────────────────────────────
    with tabs[5]:
        st.markdown(f'<div class="section-header">{t("data_header",LNG)}</div>', unsafe_allow_html=True)
        if df_raw is not None:
            fc1,fc2,fc3 = st.columns(3)
            filtered = df_raw.copy()
            with fc1:
                if "industry" in df_raw.columns:
                    sel=st.multiselect(t("filter_industry",LNG), df_raw["industry"].dropna().unique())
                    if sel: filtered=filtered[filtered["industry"].isin(sel)]
            with fc2:
                if "region" in df_raw.columns:
                    sel=st.multiselect(t("filter_region",LNG), df_raw["region"].dropna().unique())
                    if sel: filtered=filtered[filtered["region"].isin(sel)]
            with fc3:
                if "experience_level" in df_raw.columns:
                    sel=st.multiselect(t("filter_exp",LNG), df_raw["experience_level"].dropna().unique())
                    if sel: filtered=filtered[filtered["experience_level"].isin(sel)]

            st.caption(f"{t('data_showing',LNG)} {len(filtered):,} {t('data_of',LNG)} {len(df_raw):,} {t('data_records',LNG)}")
            st.dataframe(filtered.head(500), use_container_width=True, height=450)
            st.download_button(t("btn_download_csv",LNG),
                filtered.to_csv(index=False).encode("utf-8"),
                "filtered_data.csv","text/csv")
        else:
            st.info(t("no_raw_data",LNG))
