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
    data_path = Path("data/master_happiness_full.csv")
    if not data_path.exists():
        st.error("data/master_happiness_full.csv not found.")
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
        yaxis_title="Happiness Score (0-10)",
        xaxis=dict(
            tickmode='array',
            tickvals=global_avg['year'].tolist(),
            ticktext=[str(int(y)) for y in global_avg['year']],
            type='category'
        )
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.caption("Source: World Happiness Report. Use the slider below the chart to zoom into specific years.")
    st.markdown("---")
    
    st.markdown("### Understanding the World Happiness Report Model")
    if Path("whr_model.png").exists():
        st.image("whr_model.png", use_container_width=True)
    else:
        st.warning("whr_model.png not found.")
    st.markdown("---")
    
    st.markdown("### Maslow's Hierarchy Model Comparison")
    st.markdown("#### 🏔️ Maslow's Hierarchy of Needs")
    maslow_png = Path("Maslow's Hierarchy's Theory.png")
    if maslow_png.exists():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(str(maslow_png), use_container_width=True)
    else:
        st.markdown("Image not found. Using text:")
        st.markdown("""
        - **Physiological & Safety Needs** (Basic Needs: GDP, Health, Education, etc.)
        - **Love/Belonging & Esteem** (Social Connections, Trust, Recognition) – *partially covered*
        - **Self-Actualization** (Meaning, Purpose, Creativity) – *future work*
        """)
    st.markdown("#### Maslow's Hierarchy – Data Coverage (Future Scope)")
    if Path("maslow_coverage.png").exists():
        st.image("maslow_coverage.png", use_container_width=True)
    else:
        st.warning("maslow_coverage.png not found.")
    st.markdown("---")
    
    # Side‑by‑side pyramid + table (margin-top fixed at 111px)
    st.markdown("### Our Maslow‑Inspired 3‑Layer Model (Equal Weight Per Layer)")
    col_left, col_right = st.columns([1, 1.5])
    
    with col_left:
        st.markdown("""
        <div style="margin-top: 111px;">
            <div style="display: flex; flex-direction: column; align-items: center;">
                <div style="width: 55%; background-color: #e2d5f5; border: 2px solid #4a2e7a; border-radius: 12px; padding: 12px; margin: 8px 0; text-align: center; font-weight: bold;">
                    Thriving Enablers
                </div>
                <div style="width: 70%; background-color: #d1ecf1; border: 2px solid #0c5460; border-radius: 12px; padding: 12px; margin: 8px 0; text-align: center; font-weight: bold;">
                    Social Connections
                </div>
                <div style="width: 85%; background-color: #d4edda; border: 2px solid #155724; border-radius: 12px; padding: 12px; margin: 8px 0; text-align: center; font-weight: bold;">
                    Basic Needs
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        table_html = """
        <table class="clean-table">
            <tr>
                <th>Layer</th>
                <th>Present (✅)</th>
                <th>Missing / Future (❌)</th>
            </tr>
            <tr>
                <td class="layer-name">Thriving Enablers</td>
                <td class="present">✅ Internet access<br>✅ EPI<br>✅ Smoking/Alcohol<br>✅ Inactivity/Obesity</td>
                <td class="missing">❌ Creativity<br>❌ Autonomy</td>
            </tr>
            <tr>
                <td class="layer-name">Social Connections</td>
                <td class="present">✅ Social support<br>✅ GINI<br>✅ Trust composite<br>✅ Gender parity</td>
                <td class="missing">❌ Family/friends<br>❌ Community belonging<br>❌ Recognition</td>
            </tr>
            <tr>
                <td class="layer-name">Basic Needs</td>
                <td class="present">✅ GDP per capita<br>✅ Health spending<br>✅ Education spending<br>✅ Electricity access</td>
                <td class="missing">❌ Clean water<br>❌ Adequate housing</td>
            </tr>
        </table>
        <p style="font-size:0.8em; margin-top:10px;">All variables within each layer carry equal weight.</p>
        """
        st.markdown(table_html, unsafe_allow_html=True)

# ---- TAB 1: Basic Needs ----
with tabs[1]:
    st.markdown("## 🏛️ Basic Needs")
    region_list = ["All"] + sorted(df['region'].dropna().unique())
    region_basic = st.selectbox("🌍 Filter by Region", region_list, key="basic_region")
    filtered = df if region_basic == "All" else df[df['region'] == region_basic]
    vars_basic = [
        ('gdp_per_capita', 'GDP per capita (USD)', 'USD', 'World Bank'),
        ('electricity_access', 'Electricity access (% of pop.)', '%', 'World Bank'),
        ('education_spending', 'Education spending (% of GDP)', '% GDP', 'World Bank'),
        ('health_spending', 'Health spending (% of GDP)', '% GDP', 'World Bank')
    ]
    rows = [vars_basic[i:i+2] for i in range(0, len(vars_basic), 2)]
    for row in rows:
        cols = st.columns(2)
        for col, (var, label, unit, src) in zip(cols, row):
            with col:
                fig = create_corr_chart(filtered, var, label, unit, force_zero=True)
                st.plotly_chart(fig, use_container_width=True)
                st.caption(f"Source: {src}. Bars show the average value per year. The red line is the yearly correlation with happiness (r). Gaps mean fewer than 5 countries that year.")

# ---- TAB 2: Social Connections ----
with tabs[2]:
    st.markdown("## 🧱 Social Connections")
    region_list = ["All"] + sorted(df['region'].dropna().unique())
    region_social = st.selectbox("🌍 Filter by Region", region_list, key="social_region")
    filtered = df if region_social == "All" else df[df['region'] == region_social]
    fig_ss = create_corr_chart(filtered, 'social_support', 'Social support (0-1)', 'Support', force_zero=True)
    st.plotly_chart(fig_ss, use_container_width=True)
    st.caption("Source: World Happiness Report. Bars show the average value per year. The red line is the yearly correlation with happiness (r). Gaps mean fewer than 5 countries that year.")
    
    st.subheader("📊 Trust composite vs Happiness")
    if 'trust_composite' in filtered.columns:
        scat = filtered.dropna(subset=['trust_composite', 'happiness_score'])
        if not scat.empty:
            fig_tr = px.scatter(scat, x='trust_composite', y='happiness_score', hover_name='country', color='region',
                                title=f"Trust composite vs Happiness (Overall r = {scat['trust_composite'].corr(scat['happiness_score']):.2f})",
                                labels={'trust_composite':'Trust composite (0-1)', 'happiness_score':'Happiness Score'},
                                opacity=0.7, size_max=8, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_tr.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig_tr, use_container_width=True)
            st.caption("Source: WVS Wave 7 (66 countries, 2017-2023). Trust composite = average of trust in police, courts, and army. No regression line.")
        else:
            st.info("No trust data for selected region.")
    else:
        st.warning("Trust composite column not found.")
    
    fig_gini = create_corr_chart(filtered, 'gini_index', 'GINI index (0-100)', 'GINI Index', force_zero=True)
    st.plotly_chart(fig_gini, use_container_width=True)
    st.caption("Source: World Bank. Bars show the average value per year. The red line is the yearly correlation with happiness (r). Gaps mean fewer than 5 countries that year.")

# ---- TAB 3: Thriving Enablers (EPI scatter aggregated by region+year) ----
with tabs[3]:
    st.markdown("## 🌱 Thriving Enablers")
    region_list = ["All"] + sorted(df['region'].dropna().unique())
    region_thrive = st.selectbox("🌍 Filter by Region", region_list, key="thrive_region")
    filtered = df if region_thrive == "All" else df[df['region'] == region_thrive]
    fig_net = create_corr_chart(filtered, 'internet_users', 'Internet access (% of pop.)', 'Users (%)', force_zero=True)
    st.plotly_chart(fig_net, use_container_width=True)
    st.caption("Source: World Bank. Bars show the average value per year. The red line is the yearly correlation with happiness (r). Gaps mean fewer than 5 countries that year.")
    
    st.markdown("### 🧬 Health Behaviours")
    health_vars = [
        ('inactivity', 'Physical inactivity (%)', '%', 'WHO'),
        ('obesity', 'Obesity prevalence (%)', '%', 'WHO'),
        ('smoking_rate', 'Smoking rate (%)', '%', 'WHO'),
        ('alcohol_consumption', 'Alcohol consumption (litres per capita)', 'Litres', 'WHO')
    ]
    rows_h = [health_vars[i:i+2] for i in range(0, len(health_vars), 2)]
    for row in rows_h:
        cols = st.columns(2)
        for col, (var, label, unit, src) in zip(cols, row):
            with col:
                fig = create_corr_chart(filtered, var, label, unit, force_zero=True)
                st.plotly_chart(fig, use_container_width=True)
                st.caption(f"Source: {src}. Bars show the average value per year. The red line is the yearly correlation with happiness (r). Gaps mean fewer than 5 countries that year.")
    
    # Environment scatter - aggregated by region and year
    st.markdown("### 🌿 Environment")
    if 'env_composite' in filtered.columns:
        region_yearly = filtered.groupby(['region', 'year']).agg(
            env_composite=('env_composite', 'mean'),
            happiness_score=('happiness_score', 'mean')
        ).reset_index().dropna()
        if not region_yearly.empty:
            fig_env = px.scatter(region_yearly, x='env_composite', y='happiness_score', 
                                 hover_name='region', color='region',
                                 title=f"EPI Score vs Happiness (Regional averages per year, Overall r = {region_yearly['env_composite'].corr(region_yearly['happiness_score']):.2f})",
                                 labels={'env_composite':'EPI Score (0-100)', 'happiness_score':'Happiness Score'},
                                 opacity=0.7, size_max=8, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_env.update_layout(height=500)
            st.plotly_chart(fig_env, use_container_width=True)
            st.caption("Source: EPI (Yale). Each point = one region in one year (aggregated from country data). No regression line.")
        else:
            st.info("No environment data for selected region.")
    else:
        st.warning("Environment composite column not found.")

# ---- TAB 4: Our Model Insights ----
with tabs[4]:
    st.markdown("## 🏆 Our Model Insights")
    st.markdown("### Wellness Ranking (3‑Layer Equal‑Weight Model)")
    st.markdown("""
    **Methodology:** For each year, z‑scores are computed for all variables across countries.  
    Risk variables (GINI, smoking, alcohol, inactivity, obesity) are inverted so higher = better.  
    Within each layer, z‑scores are averaged; then the three layer averages are summed (equal weight per layer).  
    Countries are ranked by this sum (higher = better wellness) and compared with the official WHR rank (based on happiness score).
    """)
    if 'wellness_rank' in df.columns and 'whr_rank' in df.columns and 'rank_diff' in df.columns:
        latest_rank = df[df['year'] == latest_year].copy()
        st.subheader(f"Rank Comparison for {latest_year}")
        col_r, col_f = st.columns(2)
        with col_r:
            risers = latest_rank.nlargest(5, 'rank_diff')[['country', 'rank_diff']]
            if not risers.empty:
                fig = go.Figure(go.Bar(x=risers['rank_diff'], y=risers['country'], orientation='h', marker_color='#10b981',
                                       text=risers['rank_diff'], textposition='outside'))
                fig.update_layout(title="Biggest Risers (WHR ranks higher than wellness)", height=300)
                st.plotly_chart(fig, use_container_width=True)
                st.caption("Positive rank_diff = WHR ranks the country better than our model.")
        with col_f:
            fallers = latest_rank.nsmallest(5, 'rank_diff')[['country', 'rank_diff']]
            if not fallers.empty:
                fig = go.Figure(go.Bar(x=fallers['rank_diff'], y=fallers['country'], orientation='h', marker_color='#ef4444',
                                       text=fallers['rank_diff'], textposition='outside'))
                fig.update_layout(title="Biggest Fallers (wellness ranks higher than WHR)", height=300)
                st.plotly_chart(fig, use_container_width=True)
                st.caption("Negative rank_diff = our model ranks the country better than WHR.")
        
        # Conditional formatting for rank_diff
        styled_df = latest_rank.sort_values('wellness_rank')[['country', 'wellness_rank', 'whr_rank', 'rank_diff']].head(20).copy()
        def color_rank_diff(val):
            if val > 0:
                return 'color: green'
            elif val < 0:
                return 'color: red'
            return 'color: gray'
        styled = styled_df.style.applymap(color_rank_diff, subset=['rank_diff'])
        st.dataframe(styled, use_container_width=True)
        st.caption("Wellness rank is based on our 3‑layer model; WHR rank is from the World Happiness Report.")
        
        st.subheader("📈 Rank Change Over Time")
        regions_trend = ["All"] + sorted(df['region'].dropna().unique())
        trend_region = st.selectbox("Select Region", regions_trend, key="trend_region")
        if trend_region == "All":
            trend_df = df
        else:
            trend_df = df[df['region'] == trend_region]
        countries_in_trend = sorted(trend_df['country'].unique())
        selected_countries = st.multiselect("Select countries", countries_in_trend, default=countries_in_trend[:5], key="our_model_rank_countries")
        if selected_countries:
            rank_trend = trend_df[trend_df['country'].isin(selected_countries)].groupby(['country', 'year'])[['rank_diff']].first().reset_index()
            fig_trend = px.line(rank_trend, x='year', y='rank_diff', color='country', markers=True,
                                title="Rank Difference (WHR rank - Wellness rank) over time")
            fig_trend.update_layout(yaxis_title="Rank Difference (positive = WHR ranks higher)")
            st.plotly_chart(fig_trend, use_container_width=True)
            st.caption("Positive values mean WHR ranks the country higher than the wellness model.")
    else:
        st.warning("Pre‑computed wellness ranking columns not found.")
    
    st.markdown("### 🧬 Internal Health Web")
    if 'inactivity' in df.columns and 'obesity' in df.columns:
        st.write(f"- **Inactivity ↔ Obesity**: r = {df['inactivity'].corr(df['obesity']):.2f} (Source: WHO)")
    if 'smoking_rate' in df.columns and 'alcohol_consumption' in df.columns:
        st.write(f"- **Smoking ↔ Alcohol**: r = {df['smoking_rate'].corr(df['alcohol_consumption']):.2f} (Source: WHO)")
    st.markdown("### ⚠️ Weak Correlations in Our Model")
    weak_vars = ['gini_index', 'trust_composite']
    weak_vals = {v: df[v].corr(df['happiness_score']) for v in weak_vars if v in df.columns}
    if weak_vals:
        weak_df = pd.DataFrame(weak_vals.items(), columns=['Variable', 'Correlation (r)'])
        st.dataframe(weak_df, use_container_width=True)
        st.caption("GINI source: World Bank; Trust composite source: WVS Wave 7.")
    else:
        st.info("Weak correlation variables not available.")

# ---- TAB 5: WHR Baseline ----
with tabs[5]:
    st.markdown("## 📊 WHR Baseline")
    st.subheader("📊 Happiness by Region")
    box_data = df.dropna(subset=['region', 'happiness_score'])
    if not box_data.empty:
        fig_box = px.box(box_data, x='region', y='happiness_score', color='region',
                         title="Distribution of Happiness Scores by Region (WHR)",
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_box.update_layout(xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)
        st.caption("Source: World Happiness Report. Each box shows the spread of happiness scores in that region.")
    else:
        st.info("No region data available.")
    st.subheader("📈 Happiness Score Trends")
    region_list = ["All"] + sorted(df['region'].dropna().unique())
    region_trend_whr = st.selectbox("Select Region", region_list, key="whr_trend_region")
    if region_trend_whr == "All":
        trend_df_whr = df
    else:
        trend_df_whr = df[df['region'] == region_trend_whr]
    countries_in_trend_whr = sorted(trend_df_whr['country'].unique())
    sel_countries = st.multiselect("Select countries", countries_in_trend_whr, default=countries_in_trend_whr[:5], key="whr_baseline_countries")
    if sel_countries:
        trend_data_whr = trend_df_whr[trend_df_whr['country'].isin(sel_countries)]
        fig_trend_whr = px.line(trend_data_whr, x='year', y='happiness_score', color='country', markers=True,
                                title=f"Happiness Score Trends ({region_trend_whr})")
        fig_trend_whr.update_layout(yaxis_range=[2,8])
        st.plotly_chart(fig_trend_whr, use_container_width=True)
        st.caption("Source: World Happiness Report.")
    st.subheader("🏆 Top 10 and ⚠️ Bottom 10 Countries")
    sel_year = st.select_slider("Select Year", options=sorted(df['year'].unique()), key="whr_year")
    year_data = df[df['year'] == sel_year].copy()
    top10 = year_data.nlargest(10, 'happiness_score')[['country', 'happiness_score']].reset_index(drop=True)
    top10.index += 1
    bottom10 = year_data.nsmallest(10, 'happiness_score')[['country', 'happiness_score']].reset_index(drop=True)
    bottom10.index += 1
    col_t, col_b = st.columns(2)
    with col_t:
        st.dataframe(top10.rename(columns={'country':'Country','happiness_score':'Score'}), use_container_width=True)
    with col_b:
        st.dataframe(bottom10.rename(columns={'country':'Country','happiness_score':'Score'}), use_container_width=True)
    st.caption("Source: World Happiness Report.")
    st.subheader("📊 Top 10 & Bottom 10 Bar Charts")
    top10_sorted = year_data.nlargest(10, 'happiness_score').sort_values('happiness_score', ascending=True)
    bottom10_sorted = year_data.nsmallest(10, 'happiness_score').sort_values('happiness_score', ascending=True)
    col_left, col_right = st.columns(2)
    with col_left:
        fig_top = go.Figure(go.Bar(x=top10_sorted['happiness_score'], y=top10_sorted['country'], orientation='h',
                                   marker_color='#10b981', text=top10_sorted['happiness_score'].round(2), textposition='outside'))
        fig_top.update_layout(title=f"Top 10 Happiest ({sel_year})", xaxis_range=[0,8], height=500)
        st.plotly_chart(fig_top, use_container_width=True)
    with col_right:
        fig_bottom = go.Figure(go.Bar(x=bottom10_sorted['happiness_score'], y=bottom10_sorted['country'], orientation='h',
                                      marker_color='#ef4444', text=bottom10_sorted['happiness_score'].round(2), textposition='outside'))
        fig_bottom.update_layout(title=f"Bottom 10 Least Happy ({sel_year})", xaxis_range=[0,8], height=500)
        st.plotly_chart(fig_bottom, use_container_width=True)
    st.subheader("📡 Internet access – yearly correlation with WHR happiness")
    internet_corr = df.groupby('year').apply(lambda x: x['internet_users'].corr(x['happiness_score']) if len(x)>=5 else np.nan).reset_index()
    internet_corr.columns = ['year', 'r']
    fig_inet = px.line(internet_corr, x='year', y='r', markers=True, title="Yearly correlation: Internet access vs Happiness")
    fig_inet.update_layout(yaxis_range=[-1,1], yaxis_title="Pearson r")
    st.plotly_chart(fig_inet, use_container_width=True)
    st.caption("Source: World Bank (internet) & World Happiness Report (happiness).")
    st.subheader("🗺️ Global Happiness Score based on HBR (2016‑2024)")
    map_df = df[['country', 'year', 'happiness_score']].dropna()
    map_df['country'] = map_df['country'].replace('United States', 'United States of America')
    if not map_df.empty:
        fig_map = px.choropleth(map_df, locations="country", locationmode="country names", color="happiness_score",
                                hover_name="country", animation_frame="year", color_continuous_scale="Viridis",
                                range_color=[2,8], title="Happiness Score by Country (WHR)")
        fig_map.update_layout(height=500)
        st.plotly_chart(fig_map, use_container_width=True)
        st.caption("Source: World Happiness Report. Animated by year. White areas have missing data.")
    else:
        st.info("No map data available.")

# ---- TAB 6: Comparison (removed trendline) ----
with tabs[6]:
    st.markdown("## ⚖️ Comparison: WHR vs Our Model")
    st.subheader("WHR Rank vs. Wellness Rank")
    comp_year = st.select_slider("Select Year", options=sorted(df['year'].unique()), key="comp_year")
    comp_data = df[df['year'] == comp_year].dropna(subset=['whr_rank', 'wellness_rank'])
    if not comp_data.empty:
        fig_scatter = px.scatter(comp_data, x='whr_rank', y='wellness_rank', hover_name='country', color='region',
                                 title=f"Rank Comparison ({comp_year})",
                                 labels={'whr_rank':'WHR Rank (lower is happier)', 'wellness_rank':'Wellness Rank (lower is better)'},
                                 opacity=0.7, size_max=8, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_scatter.add_shape(type='line', x0=0, y0=0, x1=comp_data['whr_rank'].max(), y1=comp_data['wellness_rank'].max(),
                              line=dict(color='red', dash='dash'))
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.caption("Dashed line: perfect agreement. Points above the line: WHR ranks better than wellness model. Source: WHR and our model.")
    else:
        st.info("Not enough data for comparison.")
    st.subheader("Top 10 Positive / Negative Rank Differences")
    comp_data['rank_diff'] = comp_data['whr_rank'] - comp_data['wellness_rank']
    pos_diff = comp_data.nlargest(10, 'rank_diff')[['country', 'whr_rank', 'wellness_rank', 'rank_diff']]
    neg_diff = comp_data.nsmallest(10, 'rank_diff')[['country', 'whr_rank', 'wellness_rank', 'rank_diff']]
    col_pos, col_neg = st.columns(2)
    with col_pos:
        st.markdown("**WHR ranks much higher than wellness**")
        st.dataframe(pos_diff, use_container_width=True)
    with col_neg:
        st.markdown("**Wellness ranks much higher than WHR**")
        st.dataframe(neg_diff, use_container_width=True)
    st.subheader("Side‑by‑side Correlations with Happiness")
    whr_factors_all = ['gdp_per_capita', 'social_support', 'life_expectancy', 'freedom', 'generosity', 'corruption']
    whr_factors_present = [v for v in whr_factors_all if v in df.columns]
    our_vars = ['gdp_per_capita', 'health_spending', 'education_spending', 'electricity_access', 'social_support', 'gini_index', 'trust_composite', 'internet_users']
    our_vars_present = [v for v in our_vars if v in df.columns]
    whr_corr = {v: df[v].corr(df['happiness_score']) for v in whr_factors_present}
    our_corr = {v: df[v].corr(df['happiness_score']) for v in our_vars_present}
    col_whr, col_our = st.columns(2)
    with col_whr:
        st.markdown("**WHR Factors**")
        whr_df = pd.DataFrame(list(whr_corr.items()), columns=['Variable', 'Correlation (r)']).sort_values('Correlation (r)', ascending=False)
        st.dataframe(whr_df, use_container_width=True)
        st.caption("Source: World Happiness Report.")
    with col_our:
        st.markdown("**Our Model Variables**")
        our_df = pd.DataFrame(list(our_corr.items()), columns=['Variable', 'Correlation (r)']).sort_values('Correlation (r)', ascending=False)
        st.dataframe(our_df, use_container_width=True)
        st.caption("Sources: World Bank, WHO, EPI, WVS.")

# ---- TAB 7: Action ----
with tabs[7]:
    st.markdown("## 🎯 Takeaways: So What?")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="insight-card"><span style='font-size:2rem'>🤝</span><h4>Strengthen Social Support</h4><small>Social support is the strongest correlate. Invest in community and healthcare.</small></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="insight-card"><span style='font-size:2rem'>⚡</span><h4>Improve Infrastructure</h4><small>Electricity and internet are key enablers.</small></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="insight-card"><span style='font-size:2rem'>🏃</span><h4>Target Health Behaviours</h4><small>Inactivity and obesity are strongly linked. Address together.</small></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="insight-card"><span style='font-size:2rem'>📊</span><h4>Monitor Inequality</h4><small>GINI shows weak negative correlation. Still important for equity.</small></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="insight-card"><span style='font-size:2rem'>🌍</span><h4>Adapt to Regional Realities</h4><small>Social support varies widely; policies must be context‑specific.</small></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="insight-card"><span style='font-size:2rem'>📡</span><h4>Re‑evaluate Digital Priorities</h4><small>Internet correlation remains strong – a persistent driver.</small></div>""", unsafe_allow_html=True)

# ---- TAB 8: Info (logo and credits moved to top) ----
with tabs[8]:
    st.markdown("## ℹ️ About This Project")
    
    # Logo and credits at the top
    logo_path = Path("spiced_logo.png")
    if logo_path.exists():
        st.image(str(logo_path), width=200)
    else:
        st.markdown("🏫 **Spiced Academy**")
    st.markdown("### 👥 Coaches & Team")
    st.markdown("**Coaches:** Sara Maras, Alex Schirokow, Vishaki Vijay, Octavio Arnejo")
    st.markdown("**Team:** Smitha Shivaprasad · Muhsidin Rahmonov · Gabriel Ogunlana")
    st.markdown("🎓 Spiced Academy — Data Analytics & AI Capstone Project | April 2026")
    st.markdown("---")
    
    st.markdown("### 📂 Data Sources")
    st.markdown("""
    - **World Happiness Report** – Happiness scores – [link](https://worldhappiness.report)
    - **World Bank** – GDP, GINI, Electricity, Internet, Education spending, Gender parity – [link](https://data.worldbank.org)
    - **WHO** – Smoking, Alcohol, Health expenditure, Inactivity, Obesity – [link](https://www.who.int/data)
    - **EPI** – Environmental Performance Index – [link](https://epi.yale.edu)
    - **WVS Wave 7** – Trust in Police, Courts, Army – [link](https://www.worldvaluessurvey.org)
    """)
    st.markdown("### 🔬 Methodology")
    st.markdown("""
    - **3‑Layer Maslow‑inspired model** (Basic Needs, Social Connections, Thriving Enablers) – equal weight per layer.
    - **Time series charts:** Raw values; yearly r‑value line (gaps when <5 countries/year); no regression lines; y‑axis starts at 0.
    - **Wellness ranking:** Yearly z‑scores, inverted for risk variables, layer averages summed, then ranked (pre‑computed).
    - **Trust composite** = average of trust in police, courts, and army (WVS Wave 7).
    - **Gender parity** used only in wellness ranking due to sparse data (primary school enrollment, 2016 and 2018 only).
    - **Correlation does not imply causation.**
    """)
    st.markdown("### 📊 Data Transparency Note")
    st.markdown("""
    - Happiness & Basic Needs: 2016,2018,2020,2022,2024 (biennial)
    - Smoking: same years; Alcohol: 2016,2018,2020 only
    - Inactivity & Obesity: 2016-2022
    - Trust components: 2017-2023, 66 countries
    - Gender parity: limited years (2016,2018)
    - Gaps are shown as missing (no interpolation)
    """)

st.markdown("---")
st.caption("© 2026 Happiness Unpacked – Data-driven well‑being framework")