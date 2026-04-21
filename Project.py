"""
Happiness Unpacked: Maslow‑Inspired 3‑Layer Well‑Being Dashboard
Spiced Academy Capstone Project – April 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Happiness Unpacked", page_icon="🏠", layout="wide")

# ---------- Custom CSS ----------
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { padding: 8px 16px; border-radius: 8px; font-size: 1rem; font-weight: 500; }
    .stTabs [aria-selected="true"] { background-color: #3b82f6; color: white; }
    .insight-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    .insight-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .data-note { background: #fef3c7; padding: 0.8rem; border-radius: 8px; font-size: 0.8rem; color: #92400e; margin-bottom: 1rem; }
    .methodology-note { background: #e0f2fe; padding: 0.8rem; border-radius: 8px; font-size: 0.8rem; color: #075985; margin-bottom: 1rem; }
    
    /* Table styling */
    .clean-table {
        width: 100%;
        border-collapse: collapse;
        font-family: sans-serif;
    }
    .clean-table th, .clean-table td {
        border: 1px solid #ccc;
        padding: 8px 12px;
        vertical-align: top;
        text-align: left;
    }
    .clean-table th {
        background-color: #f2f2f2;
        font-weight: bold;
        text-align: center;
    }
    .present { color: #2e7d32; }
    .missing { color: #c62828; }
    .layer-name { font-weight: bold; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ---------- Data loading ----------
@st.cache_data
def load_data():
    # FIXED: Removed "data/" from the path to match your GitHub file structure
    data_path = Path("master_happiness_full.csv")
    if not data_path.exists():
        st.error("master_happiness_full.csv not found in the repository.")
        return pd.DataFrame()
    df = pd.read_csv(data_path)
    if 'health_expenditure' in df.columns and 'health_spending' not in df.columns:
        df.rename(columns={'health_expenditure': 'health_spending'}, inplace=True)
    return df

df = load_data()
if df.empty:
    st.stop()

# Dark mode & download
col_dark, col_download = st.columns([1, 5])
with col_dark:
    dark_mode = st.toggle("🌙 Dark Mode", value=False)
if dark_mode:
    st.markdown("""
    <style>
        .stApp { background-color: #0f172a; color: #f8fafc; }
        .stTabs [data-baseweb="tab-list"] { background-color: #1e293b; }
        .stTabs [data-baseweb="tab"] { color: #f8fafc; }
        .insight-card { background: linear-gradient(135deg, #334155, #1e293b); }
        .data-note { background: #451a03; color: #fde68a; }
        .methodology-note { background: #1e3a8a; color: #bfdbfe; }
        .clean-table th { background-color: #334155; color: #f8fafc; }
        .clean-table td { border-color: #555; }
        .present { color: #8fef8f; }
        .missing { color: #ff8a8a; }
    </style>
    """, unsafe_allow_html=True)
with col_download:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Data CSV", csv, "happiness_data.csv", "text/csv")

# Data transparency note
st.markdown("""
<div class="data-note">
📊 <strong>Data Transparency Note</strong><br>
• Happiness Score & Basic Needs: 2016,2018,2020,2022,2024 (biennial)<br>
• Smoking Rate: 2016,2018,2020,2022,2024<br>
• Alcohol Consumption: 2016,2018,2020 only<br>
• Physical Inactivity & Obesity: 2016-2022<br>
• Trust Components: 2017-2023, 66 countries only<br>
• Gender Parity: World Bank primary enrollment ratio (limited years, used only in wellness ranking)<br>
• Gaps shown as missing; correlation ≠ causation.
</div>
""", unsafe_allow_html=True)

# KPI row
latest_year = df['year'].max()
latest_data = df[df['year'] == latest_year].copy()
global_gini = latest_data['gini_index'].mean()
global_social_support = latest_data['social_support'].mean(skipna=True)
global_avg_happiness = latest_data['happiness_score'].mean()
top_country = latest_data.loc[latest_data['happiness_score'].idxmax(), 'country']
top_score = latest_data['happiness_score'].max()
bottom_country = latest_data.loc[latest_data['happiness_score'].idxmin(), 'country']
bottom_score = latest_data['happiness_score'].min()

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"**{global_gini:.2f}**<br>📊 Global GINI", unsafe_allow_html=True)
with col2:
    st.markdown(f"**{global_social_support:.2f}**<br>🤝 Social Support (0-1)", unsafe_allow_html=True)
with col3:
    st.markdown(f"**{global_avg_happiness:.1f}/10**<br>🌍 Global Avg", unsafe_allow_html=True)
with col4:
    st.markdown(f"**{top_score:.1f}/10**<br>🏆 {top_country}", unsafe_allow_html=True)
with col5:
    st.markdown(f"**{bottom_score:.1f}/10**<br>⚠️ {bottom_country}", unsafe_allow_html=True)

st.markdown("---")

# ---------- Dynamic correlation chart (respects region filter) ----------
def create_corr_chart(df, var, label, y_title, force_zero=True, source=""):
    if var not in df.columns:
        st.warning(f"Variable '{var}' not found. Skipping chart.")
        return go.Figure()
    
    years = sorted(df['year'].unique())
    means = []
    corrs = []
    for year in years:
        year_df = df[df['year'] == year]
        mean_val = year_df[var].mean()
        means.append({'year': year, 'value': mean_val})
        valid = year_df[[var, 'happiness_score']].dropna()
        if len(valid) >= 5:
            r = valid[var].corr(valid['happiness_score'])
            corrs.append({'year': year, 'corr': r})
        else:
            corrs.append({'year': year, 'corr': np.nan})
    
    means_df = pd.DataFrame(means)
    corrs_df = pd.DataFrame(corrs)
    
    fig = go.Figure()
    for _, row in means_df.iterrows():
        y = row['year']
        val = row['value']
        fig.add_trace(go.Bar(x=[y], y=[val], marker_color='#3b82f6', showlegend=False))
    fig.add_trace(go.Scatter(x=corrs_df['year'], y=corrs_df['corr'], mode='lines+markers', name='Yearly r-value',
                             line=dict(color='#ef4444', width=2, dash='dot'), yaxis="y2", connectgaps=False))
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, yref="y2")
    
    overall_r = df[var].corr(df['happiness_score']) if var in df.columns else np.nan
    y_range = [0, None] if force_zero else None
    fig.update_layout(
        title=f"{label} (Overall r = {overall_r:.2f})",
        xaxis_title="Year",
        yaxis=dict(title=y_title, side="left", range=y_range),
        yaxis2=dict(title="R-value", overlaying="y", side="right", range=[-1, 1]),
        height=350,
        bargap=0.3
    )
    return fig

# ---------- TABS ----------
tabs = st.tabs([
    "🏠 Intro",
    "🏛️ Basic Needs",
    "🧱 Social Connections",
    "🌱 Thriving Enablers",
    "🏆 Our Model Insights",
    "📊 WHR Baseline",
    "⚖️ Comparison",
    "🎯 Action",
    "ℹ️ Info"
])

# ---- TAB 0: Intro ----
with tabs[0]:
    st.markdown("# 🏠🏛️🧱 Happiness Unpacked")
    st.markdown("## A Data-Driven Framework for Global Well-Being")
    st.markdown(f"*Based on {df['country'].nunique()} countries (2016–2024, biennial)*")
    st.markdown("---")
    st.markdown("#### ❓ Does money really buy happiness?")
    st.markdown("#### ❓ Is it wealth? Health? Trust? Or is it truly something else?")
    st.markdown("---")
    
    # Global Happiness Trend (discrete years only)
    st.markdown("### 📈 Global Average Happiness Trend")
    global_avg = df.groupby('year')['happiness_score'].mean().reset_index()
    fig_trend = px.line(global_avg, x='year', y='happiness_score', markers=True, title="Global Happiness Over Time")
    fig_trend.update_layout(
        yaxis_range=[5, 6],
        xaxis_title="Year",
        yaxis_title="Happiness Score (0-10)")
