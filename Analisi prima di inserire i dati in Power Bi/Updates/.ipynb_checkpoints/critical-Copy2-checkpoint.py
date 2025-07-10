# ============================================================================
# STARTUP ECOSYSTEM DASHBOARD - MIDNIGHT PULSE EDITION
# ============================================================================
# Dashboard critico con i dati reali del Registro Imprese + Crunchbase
# Tema: Midnight Pulse - Interfaccia Futuristica Cyber
# 
# FILES NECESSARI:
# - clean_dataset.xlsx (Registro Imprese pulito)
# - da vedere.xlsx (Crunchbase data)
# - Prevalenza.xlsx (Legende)
#
# INSTALLAZIONE:
# pip install streamlit plotly pandas numpy openpyxl
# 
# ESECUZIONE:
# streamlit run futuristic_startup_dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURAZIONE PAGINA
# ============================================================================

st.set_page_config(
    page_title="🚀 Startup Reality Matrix",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 🎨 MIDNIGHT PULSE THEME - FUTURISTIC CSS
# ============================================================================

st.markdown("""
<style>
    /* GLOBAL FUTURISTIC THEME */
    .stApp {
        background: linear-gradient(135deg, #0f0f10 0%, #1a1a1b 50%, #0f0f10 100%);
        background-attachment: fixed;
    }
    
    /* CYBER GRID BACKGROUND */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(142, 68, 173, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(142, 68, 173, 0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: -1;
    }
    
    /* FUTURISTIC METRIC CARDS */
    .cyber-metric {
        background: linear-gradient(135deg, rgba(142, 68, 173, 0.2) 0%, rgba(15, 15, 16, 0.9) 100%);
        border: 2px solid rgba(142, 68, 173, 0.5);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 0.5rem 0;
        box-shadow: 
            0 0 30px rgba(142, 68, 173, 0.3),
            inset 0 0 20px rgba(209, 60, 224, 0.1);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .cyber-metric::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #8e44ad, #d13ce0, #8e44ad);
        border-radius: 20px;
        z-index: -1;
        animation: borderGlow 3s linear infinite;
    }
    
    @keyframes borderGlow {
        0%, 100% { transform: rotate(0deg); }
        50% { transform: rotate(180deg); }
    }
    
    .critical-metric {
        background: linear-gradient(135deg, rgba(209, 60, 224, 0.3) 0%, rgba(15, 15, 16, 0.9) 100%);
        border: 2px solid #d13ce0;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 0.5rem 0;
        box-shadow: 
            0 0 40px rgba(209, 60, 224, 0.5),
            inset 0 0 20px rgba(209, 60, 224, 0.2);
        backdrop-filter: blur(15px);
    }
    
    .success-metric {
        background: linear-gradient(135deg, rgba(0, 255, 159, 0.2) 0%, rgba(15, 15, 16, 0.9) 100%);
        border: 2px solid #00ff9f;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 0.5rem 0;
        box-shadow: 
            0 0 30px rgba(0, 255, 159, 0.3),
            inset 0 0 20px rgba(0, 255, 159, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .warning-metric {
        background: linear-gradient(135deg, rgba(142, 68, 173, 0.25) 0%, rgba(15, 15, 16, 0.9) 100%);
        border: 2px solid #8e44ad;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 0.5rem 0;
        box-shadow: 
            0 0 30px rgba(142, 68, 173, 0.4),
            inset 0 0 20px rgba(142, 68, 173, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* HOLOGRAPHIC TEXT EFFECTS */
    .metric-title {
        color: #e0e0e0;
        font-size: 0.9rem;
        margin: 0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(224, 224, 224, 0.5);
    }
    
    .metric-value {
        color: #00ff9f;
        font-size: 2.5rem;
        margin: 0.3rem 0;
        font-weight: bold;
        text-shadow: 0 0 20px rgba(0, 255, 159, 0.8);
        font-family: 'Courier New', monospace;
    }
    
    .critical-value {
        color: #d13ce0;
        font-size: 2.5rem;
        margin: 0.3rem 0;
        font-weight: bold;
        text-shadow: 0 0 20px rgba(209, 60, 224, 0.8);
        font-family: 'Courier New', monospace;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .metric-subtitle {
        color: rgba(224, 224, 224, 0.7);
        font-size: 0.8rem;
        margin: 0;
        text-shadow: 0 0 5px rgba(224, 224, 224, 0.3);
    }
    
    /* CYBER ANALYSIS BOXES */
    .cyber-analysis {
        background: linear-gradient(135deg, rgba(15, 15, 16, 0.95) 0%, rgba(142, 68, 173, 0.1) 100%);
        border: 1px solid rgba(142, 68, 173, 0.3);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 
            0 0 25px rgba(142, 68, 173, 0.2),
            inset 0 0 15px rgba(209, 60, 224, 0.05);
        backdrop-filter: blur(8px);
    }
    
    /* NEON HEADERS */
    .neon-header {
        color: #00ff9f;
        text-shadow: 
            0 0 5px #00ff9f,
            0 0 10px #00ff9f,
            0 0 15px #00ff9f,
            0 0 20px #00ff9f;
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    
    .cyber-title {
        color: #d13ce0;
        text-shadow: 
            0 0 5px #d13ce0,
            0 0 10px #d13ce0,
            0 0 15px #d13ce0;
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* FUTURISTIC SCROLLBARS */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 15, 16, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #8e44ad, #d13ce0);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #d13ce0, #00ff9f);
    }
    
    /* HOLOGRAPHIC TABLES */
    .dataframe {
        background: rgba(15, 15, 16, 0.8) !important;
        border: 1px solid rgba(142, 68, 173, 0.3) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* CYBER BUTTONS */
    .stButton > button {
        background: linear-gradient(45deg, #8e44ad, #d13ce0);
        color: #e0e0e0;
        border: none;
        border-radius: 15px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 0 20px rgba(142, 68, 173, 0.5);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #d13ce0, #00ff9f);
        box-shadow: 0 0 30px rgba(0, 255, 159, 0.7);
        transform: translateY(-2px);
    }
    
    /* SIDEBAR CYBER STYLING */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(15, 15, 16, 0.95) 0%, rgba(142, 68, 173, 0.1) 100%);
        border-right: 2px solid rgba(142, 68, 173, 0.3);
    }
    
    /* CYBER SELECTBOX */
    .stSelectbox > div > div {
        background: rgba(15, 15, 16, 0.8);
        border: 1px solid rgba(142, 68, 173, 0.5);
        border-radius: 10px;
    }
    
    /* LOADING SPINNER CYBER */
    .stSpinner > div {
        border-color: #8e44ad #d13ce0 #00ff9f #8e44ad;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CARICAMENTO DATI REALI
# ============================================================================

@st.cache_data
def load_real_data():
    """
    Carica i dati REALI dai file che abbiamo analizzato
    """
    try:
        # 1. DATASET REGISTRO IMPRESE PULITO
        st.write("🔄 **Inizializzazione Matrix Startup...**")
        df_ri = pd.read_excel('clean_dataset.xlsx')
        st.write(f"✅ **Neural Network RI**: {len(df_ri)} entità caricate")
        
        # 2. DATASET CRUNCHBASE  
        st.write("💾 **Connecting to Crunchbase Database...**")
        df_cb = pd.read_excel('da vedere.xlsx', sheet_name='Startup_Italia_2020_2025')
        st.write(f"✅ **Funding Matrix**: {len(df_cb)} records sincronizzati")
        
        # 3. LEGENDE
        st.write("📡 **Loading Reference Data...**")
        try:
            df_legenda_prod = pd.read_excel('Prevalenza.xlsx', sheet_name='Classe di produzione')
            df_legenda_add = pd.read_excel('Prevalenza.xlsx', sheet_name='Classe di Addetti') 
            df_legenda_cap = pd.read_excel('Prevalenza.xlsx', sheet_name='Classe di Capitale')
        except:
            st.warning("⚠️ **Sistema Prevalenza offline**, continuando in modalità limitata")
            df_legenda_prod = df_legenda_add = df_legenda_cap = pd.DataFrame()
        
        return df_ri, df_cb, df_legenda_prod, df_legenda_add, df_legenda_cap
        
    except Exception as e:
        st.error(f"❌ **CRITICAL ERROR**: Matrix disconnessa - {e}")
        st.error("**Required Files**:")
        st.error("- clean_dataset.xlsx")  
        st.error("- da vedere.xlsx")
        st.error("- Prevalenza.xlsx (opzionale)")
        return None, None, None, None, None

# ============================================================================
# CYBER HEADER
# ============================================================================

st.markdown("""
<div style='text-align: center; background: linear-gradient(135deg, rgba(209, 60, 224, 0.3) 0%, rgba(15, 15, 16, 0.9) 50%, rgba(0, 255, 159, 0.2) 100%); 
     padding: 3rem; border-radius: 25px; margin-bottom: 2rem; 
     box-shadow: 0 0 50px rgba(142, 68, 173, 0.4), inset 0 0 30px rgba(209, 60, 224, 0.1);
     border: 2px solid rgba(142, 68, 173, 0.5); backdrop-filter: blur(15px);'>
    <h1 class='neon-header' style='margin: 0; font-size: 3rem;'>🚀 STARTUP REALITY MATRIX</h1>
    <h3 class='cyber-title' style='margin: 0.5rem 0; font-size: 1.5rem;'>⚡ Neural Network Analysis</h3>
    <p style='color: #e0e0e0; margin: 0; font-family: Courier New; letter-spacing: 1px;'>
        🔬 REGISTRO IMPRESE • 💾 CRUNCHBASE • 🎯 2020-2025
    </p>
</div>
""", unsafe_allow_html=True)

# Carica i dati
data_loaded = False
with st.spinner("🔄 **Connecting to Matrix...**"):
    df_ri, df_cb, df_legenda_prod, df_legenda_add, df_legenda_cap = load_real_data()
    
    if df_ri is not None and df_cb is not None:
        data_loaded = True
        st.success(f"✅ **Matrix Online**: {len(df_ri)} startup RI + {len(df_cb)} entità CB")

if not data_loaded:
    st.stop()

# ============================================================================
# ANALISI E PREPARAZIONE DATI CRITICI - VERSIONE CORRETTA
# ============================================================================

@st.cache_data
def prepare_critical_analysis(df_ri, df_cb):
    """
    Prepara le analisi critiche con i dati reali - VERSIONE CORRETTA
    """
    
    # 1. ANALISI MORTALITÀ REALE
    mortality_stats = {
        'total_startups': len(df_ri),
        'active_startups': len(df_ri[df_ri['stato'] == 'attiva']),
        'liquidated_startups': len(df_ri[df_ri['stato'] == 'in liquidazione']),
        'mortality_rate': len(df_ri[df_ri['stato'] == 'in liquidazione']) / len(df_ri) * 100
    }
    
    # 2. ANALISI SETTORIALE CRITICA
    sector_analysis = df_ri.groupby('settore').agg({
        'denominazione': 'count',
        'stato': lambda x: (x == 'in liquidazione').sum(),
    }).rename(columns={'denominazione': 'total', 'stato': 'liquidated'})
    
    sector_analysis['failure_rate'] = (sector_analysis['liquidated'] / sector_analysis['total'] * 100).round(2)
    sector_analysis = sector_analysis.sort_values('failure_rate', ascending=False)
    
    # 3. ANALISI GEOGRAFICA CRITICA
    geo_analysis = df_ri.groupby('pv').agg({
        'denominazione': 'count',
        'stato': lambda x: (x == 'in liquidazione').sum(),
    }).rename(columns={'denominazione': 'total', 'stato': 'liquidated'})
    
    geo_analysis['failure_rate'] = (geo_analysis['liquidated'] / geo_analysis['total'] * 100).round(2)
    geo_analysis = geo_analysis[geo_analysis['total'] >= 10]
    geo_analysis = geo_analysis.sort_values('failure_rate', ascending=False)
    
    # 4. MATCHING CRUNCHBASE - REGISTRO IMPRESE
    st.write("🔄 **Neural Matching in Progress...**")
    
    def clean_name_for_matching(name):
        if pd.isna(name):
            return ''
        return str(name).lower().replace(' ', '').replace('-', '').replace('.', '').replace(',', '')
    
    cb_mapping = {}
    for idx, row in df_cb.iterrows():
        clean_name = clean_name_for_matching(row['Organization Name'])
        if len(clean_name) > 3:
            cb_mapping[clean_name] = {
                'funding_usd': row.get('Total Funding Amount (in USD)', 0) if pd.notna(row.get('Total Funding Amount (in USD)', 0)) else 0,
                'funding_rounds': row.get('Number of Funding Rounds', 0) if pd.notna(row.get('Number of Funding Rounds', 0)) else 0,
                'last_funding_type': row.get('Last Funding Type', '') if pd.notna(row.get('Last Funding Type', '')) else '',
                'investors': row.get('Top 5 Investors', '') if pd.notna(row.get('Top 5 Investors', '')) else '',
                'employees': row.get('Number of Employees', '') if pd.notna(row.get('Number of Employees', '')) else '',
                'revenue_range': row.get('Estimated Revenue Range', '') if pd.notna(row.get('Estimated Revenue Range', '')) else ''
            }
    
    funding_matches = []
    for idx, row in df_ri.iterrows():
        clean_name = clean_name_for_matching(row['denominazione'])
        if clean_name in cb_mapping:
            match_data = cb_mapping[clean_name].copy()
            match_data.update({
                'ri_name': row['denominazione'],
                'ri_sector': row['settore'],
                'ri_province': row['pv'],
                'ri_status': row['stato']
            })
            funding_matches.append(match_data)
    
    funding_df = pd.DataFrame(funding_matches)
    
    # 5. ANALISI FUNDING CRITICA
    funding_stats = {
        'total_ri_startups': len(df_ri),
        'matched_with_cb': len(funding_df),
        'matching_rate': len(funding_df) / len(df_ri) * 100,
        'funded_startups': len(funding_df[funding_df['funding_usd'] > 0]) if len(funding_df) > 0 else 0,
        'funding_success_rate': len(funding_df[funding_df['funding_usd'] > 0]) / len(df_ri) * 100 if len(funding_df) > 0 else 0,
        'avg_funding': funding_df[funding_df['funding_usd'] > 0]['funding_usd'].mean() if len(funding_df) > 0 and len(funding_df[funding_df['funding_usd'] > 0]) > 0 else 0,
        'total_funding': funding_df['funding_usd'].sum() if len(funding_df) > 0 else 0,
        'mega_funded': len(funding_df[funding_df['funding_usd'] > 1000000]) if len(funding_df) > 0 else 0,
        'failed_funded': len(funding_df[(funding_df['funding_usd'] > 0) & (funding_df['ri_status'] == 'in liquidazione')]) if len(funding_df) > 0 else 0
    }
    
    # 6. ANALISI TEMPORALE
    try:
        df_ri['data_iscrizione_startup'] = pd.to_datetime(df_ri['data iscrizione alla sezione delle startup'], errors='coerce')
        df_ri_valid_dates = df_ri.dropna(subset=['data_iscrizione_startup'])
        
        if len(df_ri_valid_dates) > 0:
            df_ri_valid_dates['year'] = df_ri_valid_dates['data_iscrizione_startup'].dt.year
            df_ri_valid_dates['quarter'] = df_ri_valid_dates['data_iscrizione_startup'].dt.quarter
            df_ri_valid_dates['year_quarter'] = df_ri_valid_dates['year'].astype(str) + 'Q' + df_ri_valid_dates['quarter'].astype(str)
            
            timeline_data = df_ri_valid_dates.groupby(['year', 'quarter']).agg({
                'denominazione': 'count',
                'stato': lambda x: (x == 'in liquidazione').sum()
            }).rename(columns={'denominazione': 'startups_founded', 'stato': 'failures'})
            
            timeline_data = timeline_data.reset_index()
            timeline_data['year_quarter'] = timeline_data['year'].astype(str) + 'Q' + timeline_data['quarter'].astype(str)
            timeline_data['growth_rate'] = timeline_data['startups_founded'].pct_change() * 100
            timeline_data = timeline_data[(timeline_data['year'] >= 2015) & (timeline_data['year'] <= 2025)]
        else:
            timeline_data = pd.DataFrame()
    except:
        timeline_data = pd.DataFrame()
    
    return mortality_stats, sector_analysis, geo_analysis, funding_df, funding_stats, timeline_data

# Prepara analisi
with st.spinner("🧠 **Neural Processing...**"):
    mortality_stats, sector_analysis, geo_analysis, funding_df, funding_stats, timeline_data = prepare_critical_analysis(df_ri, df_cb)

# ============================================================================
# CYBER SIDEBAR - NEURAL INTERFACE
# ============================================================================

st.sidebar.markdown("## 🎯 NEURAL INTERFACE")

analysis_type = st.sidebar.selectbox(
    "🔮 **Select Analysis Mode**",
    ["🚨 Matrix Overview", "💀 Mortality Scan", "💸 Funding Reality", 
     "🏭 Sector Risk Assessment", "📍 Geographic Threat Map", "📊 Timeline Analysis"],
    help="Choose your analysis perspective"
)

if len(sector_analysis) > 0:
    critical_threshold = st.sidebar.slider(
        "⚡ **Critical Alert Threshold**",
        min_value=0.5, max_value=10.0, value=2.0, step=0.1,
        help="Set the risk threshold for critical alerts"
    )

show_details = st.sidebar.checkbox("📋 **Display Data Tables**", value=True)

# Cyber Status Panel
st.sidebar.markdown(f"""
<div class="cyber-analysis">
    <h4 class="cyber-title">🔬 SYSTEM STATUS</h4>
    <ul style="color: #e0e0e0; font-family: 'Courier New';">
        <li>🔋 **Neural Network**: <span style="color: #00ff9f;">ONLINE</span></li>
        <li>📡 **Data Stream**: <span style="color: #00ff9f;">ACTIVE</span></li>
        <li>🎯 **Analysis**: <span style="color: #d13ce0;">RUNNING</span></li>
        <li>⚡ **Matrix Load**: <span style="color: #8e44ad;">OPTIMAL</span></li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# MAIN CYBER DASHBOARD
# ============================================================================

if analysis_type == "🚨 Matrix Overview":
    
    st.markdown("## 🚨 MATRIX OVERVIEW PROTOCOL")
    
    # Cyber metriche principali
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="critical-metric">
            <h3 class="metric-title">💀 MORTALITY RATE</h3>
            <h2 class="critical-value">{mortality_stats['mortality_rate']:.2f}%</h2>
            <p class="metric-subtitle">{mortality_stats['liquidated_startups']} entities terminated</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="critical-metric">
            <h3 class="metric-title">🏜️ FUNDING DESERT</h3>
            <h2 class="critical-value">{100 - funding_stats['funding_success_rate']:.1f}%</h2>
            <p class="metric-subtitle">Zero external funding</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        survival_rate = 100 - mortality_stats['mortality_rate']
        metric_class = "warning-metric" if survival_rate < 95 else "success-metric"
        st.markdown(f"""
        <div class="{metric_class}">
            <h3 class="metric-title">💚 SURVIVAL RATE</h3>
            <h2 class="metric-value">{survival_rate:.1f}%</h2>
            <p class="metric-subtitle">{mortality_stats['active_startups']} active entities</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="cyber-metric">
            <h3 class="metric-title">🎯 NEURAL MATCH</h3>
            <h2 class="metric-value">{funding_stats['matching_rate']:.1f}%</h2>
            <p class="metric-subtitle">{funding_stats['matched_with_cb']} / {funding_stats['total_ri_startups']} synced</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Matrix Risk Analysis
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 **THREAT ASSESSMENT MATRIX**")
        
        sector_risk_data = sector_analysis.reset_index()
        sector_risk_data = sector_risk_data[sector_risk_data['total'] >= 30]
        
        if len(sector_risk_data) > 0:
            fig = go.Figure()
            
            # Cyber color scheme
            colors = []
            for x in sector_risk_data['failure_rate']:
                if x > critical_threshold:
                    colors.append('#d13ce0')  # Critical magenta
                elif x > 1:
                    colors.append('#8e44ad')  # Warning purple
                else:
                    colors.append('#00ff9f')  # Safe green
            
            fig.add_trace(go.Scatter(
                x=sector_risk_data['total'],
                y=sector_risk_data['failure_rate'],
                mode='markers+text',
                text=sector_risk_data['settore'],
                textposition="top center",
                marker=dict(
                    size=sector_risk_data['liquidated'] * 15 + 25,
                    color=colors,
                    line=dict(width=3, color='#e0e0e0'),
                    opacity=0.8
                ),
                hovertemplate="<b>%{text}</b><br>" +
                              "Total Entities: %{x}<br>" +
                              "Failure Rate: %{y}%<br>" +
                              "Terminated: %{marker.size}<br>" +
                              "<extra></extra>"
            ))
            
            # Critical threshold line
            fig.add_hline(y=critical_threshold, line_dash="dash", line_color="#d13ce0", 
                         annotation_text=f"CRITICAL THRESHOLD {critical_threshold}%",
                         annotation_font_color="#d13ce0")
            
            fig.update_layout(
                title=dict(text="Sector Risk Matrix", font=dict(color='#e0e0e0', size=16)),
                xaxis_title="Total Startup Entities",
                yaxis_title="Failure Rate %",
                height=500,
                plot_bgcolor='rgba(15,15,16,0.8)',
                paper_bgcolor='rgba(15,15,16,0)',
                font=dict(color='#e0e0e0'),
                xaxis=dict(gridcolor='rgba(142, 68, 173, 0.2)'),
                yaxis=dict(gridcolor='rgba(142, 68, 173, 0.2)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ **Insufficient data for risk matrix generation**")
    
    with col2:
        st.markdown("### ⚡ **CRITICAL ALERTS**")
        
        # Settori sopra soglia critica
        critical_sectors = sector_analysis[sector_analysis['failure_rate'] > critical_threshold]
        
        if len(critical_sectors) > 0:
            st.markdown(f"""
            <div class="cyber-analysis">
                <h4 class="cyber-title">🔴 HIGH RISK SECTORS</h4>
            """, unsafe_allow_html=True)
            
            for sector, data in critical_sectors.iterrows():
                failure_rate = data['failure_rate']
                active_count = data['total'] - data['liquidated']
                
                st.markdown(f"""
                <div style='background: rgba(209, 60, 224, 0.1); padding: 1rem; border-radius: 15px; margin: 0.5rem 0; border: 1px solid rgba(209, 60, 224, 0.3);'>
                    <h4 style='color: #d13ce0; margin: 0;'>💥 {sector}</h4>
                    <ul style='color: #e0e0e0; font-family: Courier New; margin: 0.5rem 0;'>
                        <li>Failure rate: <strong style="color:#d13ce0;">{failure_rate:.1f}%</strong></li>
                        <li>Active entities: <strong style="color:#00ff9f;">{active_count}</strong></li>
                        <li>Terminated: <strong style="color:#d13ce0;">{data['liquidated']}</strong></li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.success("✅ **No sectors above critical threshold**")
        
        # Province più rischiose  
        critical_provinces = geo_analysis.head(5)
        
        if len(critical_provinces) > 0:
            st.markdown(f"""
            <div class="cyber-analysis">
                <h4 style="color: #8e44ad;">⚠️ HIGH RISK PROVINCES</h4>
            """, unsafe_allow_html=True)
            
            for prov, data in critical_provinces.iterrows():
                st.markdown(f"""
                <div style="background: rgba(142, 68, 173, 0.1); padding: 0.8rem; margin: 0.5rem 0; border-radius: 8px; border: 1px solid rgba(142, 68, 173, 0.3);">
                    <strong style="color: #8e44ad;">{prov}</strong>: {data['failure_rate']:.1f}%<br>
                    <small style="color: #e0e0e0;">{data['liquidated']}/{data['total']} entities</small>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Funding stats
        st.markdown(f"""
        <div class="cyber-analysis">
            <h4 style="color: #00ff9f;">💰 FUNDING MATRIX</h4>
            <ul style="color: #e0e0e0; font-family: 'Courier New';">
                <li>Funded entities: <strong style="color:#00ff9f;">{funding_stats['funded_startups']}</strong></li>
                <li>Success rate: <strong style="color:#8e44ad;">{funding_stats['funding_success_rate']:.1f}%</strong></li>
                <li>Average funding: <strong style="color:#d13ce0;">${funding_stats['avg_funding']:,.0f}</strong></li>
                <li>Mega funded (>$1M): <strong style="color:#00ff9f;">{funding_stats['mega_funded']}</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif analysis_type == "💀 Mortality Scan":
    
    st.markdown("## 💀 **MORTALITY SCAN PROTOCOL**")
    
    # Statistiche mortalità dettagliate
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="critical-metric">
            <h3 class="metric-title">💀 TERMINATED</h3>
            <h2 class="critical-value">{mortality_stats['liquidated_startups']}</h2>
            <p class="metric-subtitle">{mortality_stats['mortality_rate']:.2f}% of total matrix</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="success-metric">
            <h3 class="metric-title">💚 ACTIVE ENTITIES</h3>
            <h2 class="metric-value">{mortality_stats['active_startups']}</h2>
            <p class="metric-subtitle">{100-mortality_stats['mortality_rate']:.2f}% survival rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if len(sector_analysis) > 0:
            worst_sector = sector_analysis.iloc[0]
            st.markdown(f"""
            <div class="critical-metric">
                <h3 class="metric-title">🏭 HIGHEST RISK</h3>
                <h2 class="critical-value">{worst_sector.name[:12]}...</h2>
                <p class="metric-subtitle">{worst_sector['failure_rate']:.1f}% failure rate</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        if len(geo_analysis) > 0:
            worst_province = geo_analysis.iloc[0]
            st.markdown(f"""
            <div class="warning-metric">
                <h3 class="metric-title">📍 DANGER ZONE</h3>
                <h2 class="metric-value">{worst_province.name}</h2>
                <p class="metric-subtitle">{worst_province['failure_rate']:.1f}% mortality</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Analisi settoriale mortalità
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏭 **SECTOR MORTALITY ANALYSIS**")
        
        if len(sector_analysis) > 0:
            fig = go.Figure()
            
            # Cyber colors per failure rate
            colors = []
            for x in sector_analysis['failure_rate']:
                if x > critical_threshold:
                    colors.append('#d13ce0')
                elif x > 1:
                    colors.append('#8e44ad')
                else:
                    colors.append('#00ff9f')
            
            fig.add_trace(go.Bar(
                y=sector_analysis.index,
                x=sector_analysis['failure_rate'],
                orientation='h',
                marker_color=colors,
                text=sector_analysis['failure_rate'].round(2),
                textposition='auto',
                marker_line=dict(color='#e0e0e0', width=1)
            ))
            
            fig.update_layout(
                title=dict(text="Failure Rate by Sector", font=dict(color='#e0e0e0')),
                xaxis_title="Failure Rate %",
                yaxis_title="Sector",
                height=400,
                plot_bgcolor='rgba(15,15,16,0.8)',
                paper_bgcolor='rgba(15,15,16,0)',
                font=dict(color='#e0e0e0'),
                xaxis=dict(gridcolor='rgba(142, 68, 173, 0.2)'),
                yaxis=dict(gridcolor='rgba(142, 68, 173, 0.2)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ **Sector data unavailable**")
    
    with col2:
        st.markdown("### 📍 **GEOGRAPHIC THREAT MAP**")
        
        if len(geo_analysis) > 0:
            top_provinces = geo_analysis.head(10)
            
            fig = go.Figure()
            
            colors = []
            for x in top_provinces['failure_rate']:
                if x > critical_threshold:
                    colors.append('#d13ce0')
                elif x > 1:
                    colors.append('#8e44ad')
                else:
                    colors.append('#00ff9f')
            
            fig.add_trace(go.Bar(
                y=top_provinces.index,
                x=top_provinces['failure_rate'],
                orientation='h',
                marker_color=colors,
                text=top_provinces['failure_rate'].round(2),
                textposition='auto',
                marker_line=dict(color='#e0e0e0', width=1)
            ))
            
            fig.update_layout(
                title=dict(text="Top 10 High-Risk Provinces", font=dict(color='#e0e0e0')),
                xaxis_title="Failure Rate %",
                yaxis_title="Province",
                height=400,
                plot_bgcolor='rgba(15,15,16,0.8)',
                paper_bgcolor='rgba(15,15,16,0)',
                font=dict(color='#e0e0e0'),
                xaxis=dict(gridcolor='rgba(142, 68, 173, 0.2)'),
                yaxis=dict(gridcolor='rgba(142, 68, 173, 0.2)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ **Geographic data unavailable**")
    
    # Dettagli tabellari se richiesti
    if show_details:
        st.markdown("### 📊 **DETAILED MORTALITY DATA**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📋 Sector Mortality Matrix**")
            if len(sector_analysis) > 0:
                sector_display = sector_analysis.reset_index()
                sector_display.columns = ['Sector', 'Total', 'Terminated', 'Rate %']
                st.dataframe(sector_display, use_container_width=True)
        
        with col2:
            st.markdown("**📋 Geographic Mortality Matrix**")
            if len(geo_analysis) > 0:
                geo_display = geo_analysis.head(15).reset_index()
                geo_display.columns = ['Province', 'Total', 'Terminated', 'Rate %']
                st.dataframe(geo_display, use_container_width=True)

elif analysis_type == "💸 Funding Reality":
    
    st.markdown("## 💸 **FUNDING ECOSYSTEM REALITY**")
    
    # Metriche funding
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="cyber-metric">
            <h3 class="metric-title">🎯 NEURAL MATCH</h3>
            <h2 class="metric-value">{funding_stats['matching_rate']:.1f}%</h2>
            <p class="metric-subtitle">{funding_stats['matched_with_cb']} / {funding_stats['total_ri_startups']} synced</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="success-metric">
            <h3 class="metric-title">💰 FUNDED ENTITIES</h3>
            <h2 class="metric-value">{funding_stats['funded_startups']}</h2>
            <p class="metric-subtitle">{funding_stats['funding_success_rate']:.1f}% of RI total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="warning-metric">
            <h3 class="metric-title">💸 AVG FUNDING</h3>
            <h2 class="metric-value">${funding_stats['avg_funding']:,.0f}</h2>
            <p class="metric-subtitle">Per funded entity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="critical-metric">
            <h3 class="metric-title">🏆 MEGA FUNDED</h3>
            <h2 class="critical-value">{funding_stats['mega_funded']}</h2>
            <p class="metric-subtitle">>$1M funding secured</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Analisi funding dettagliata
    if len(funding_df) > 0:
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💰 **FUNDING DISTRIBUTION MATRIX**")
            
            # Segmenta funding per livelli
            funding_df['funding_segment'] = funding_df['funding_usd'].apply(
                lambda x: 'No Funding' if x == 0 else
                         'Micro (<$100K)' if x < 100000 else
                         'Small ($100K-$1M)' if x < 1000000 else
                         'Medium ($1M-$10M)' if x < 10000000 else
                         'Large (>$10M)'
            )
            
            funding_distribution = funding_df['funding_segment'].value_counts()
            
            fig = go.Figure()
            
            # Cyber colors per funding levels
            colors = {
                'No Funding': '#d13ce0', 
                'Micro (<$100K)': '#8e44ad', 
                'Small ($100K-$1M)': '#00ff9f', 
                'Medium ($1M-$10M)': '#e0e0e0',
                'Large (>$10M)': '#0f0f10'
            }
            
            fig.add_trace(go.Pie(
                labels=funding_distribution.index,
                values=funding_distribution.values,
                marker_colors=[colors.get(x, '#888888') for x in funding_distribution.index],
                hole=0.4,
                textfont=dict(color='#e0e0e0', size=12)
            ))
            
            fig.update_layout(
                title=dict(text="Funding Level Distribution", font=dict(color='#e0e0e0')),
                height=400,
                plot_bgcolor='rgba(15,15,16,0.8)',
                paper_bgcolor='rgba(15,15,16,0)',
                font=dict(color='#e0e0e0')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🏭 **SECTOR FUNDING ANALYSIS**")
            
            # Analisi funding per settore - usando la stessa logica del codice funzionante
            sector_funding = funding_df.groupby('ri_sector').agg({
                'funding_usd': ['count', 'mean', 'sum'],
                'ri_name': 'count'
            }).round(0)
            
            sector_funding.columns = ['funded_count', 'avg_funding', 'total_funding', 'total_startups']
            sector_funding['funding_rate'] = (sector_funding['funded_count'] / sector_funding['total_startups'] * 100).round(1)
            sector_funding = sector_funding.sort_values('avg_funding', ascending=True)
            
            # Rimuovi NaN
            sector_funding = sector_funding.dropna()
            
            if len(sector_funding) > 0:
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    y=sector_funding.index,
                    x=sector_funding['avg_funding'],
                    orientation='h',
                    marker_color='#00ff9f',
                    text=sector_funding['avg_funding'].fillna(0).astype(int),
                    textposition='auto',
                    marker_line=dict(color='#e0e0e0', width=1)
                ))
                
                fig.update_layout(
                    title=dict(text="Average Funding by Sector", font=dict(color='#e0e0e0')),
                    xaxis_title="Average Funding (USD)",
                    yaxis_title="Sector",
                    height=400,
                    plot_bgcolor='rgba(15,15,16,0.8)',
                    paper_bgcolor='rgba(15,15,16,0)',
                    font=dict(color='#e0e0e0'),
                    xaxis=dict(gridcolor='rgba(142, 68, 173, 0.2)'),
                    yaxis=dict(gridcolor='rgba(142, 68, 173, 0.2)')
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ **Sector funding data unavailable**")
        
        # Top funded startups
        st.markdown("### 🏆 **ELITE FUNDED ENTITIES**")
        
        top_funded = funding_df[funding_df['funding_usd'] > 0].nlargest(10, 'funding_usd')
        
        if len(top_funded) > 0:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    y=top_funded['ri_name'].str[:30],
                    x=top_funded['funding_usd'] / 1000000,  # Convert to millions
                    orientation='h',
                    marker_color='#00ff9f',
                    text=(top_funded['funding_usd'] / 1000000).round(1),
                    textposition='auto',
                    marker_line=dict(color='#e0e0e0', width=1)
                ))
                
                fig.update_layout(
                    title=dict(text="Top 10 Entities by Funding (Million USD)", font=dict(color='#e0e0e0')),
                    xaxis_title="Funding (Million USD)",
                    yaxis_title="Entity",
                    height=500,
                    plot_bgcolor='rgba(15,15,16,0.8)',
                    paper_bgcolor='rgba(15,15,16,0)',
                    font=dict(color='#e0e0e0'),
                    xaxis=dict(gridcolor='rgba(142, 68, 173, 0.2)'),
                    yaxis=dict(gridcolor='rgba(142, 68, 173, 0.2)')
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("**💎 Elite Entity Details**")
                for idx, row in top_funded.head(5).iterrows():
                    st.markdown(f"""
                    <div class="cyber-analysis">
                        <strong style="color: #00ff9f;">{row['ri_name'][:25]}...</strong><br>
                        💰 ${row['funding_usd']/1000000:.1f}M<br>
                        🏭 {row['ri_sector']}<br>
                        📍 {row['ri_province']}
                    </div>
                    """, unsafe_allow_html=True)
    
    else:
        st.warning("⚠️ **No neural matches found between RI and Crunchbase matrices**")

elif analysis_type == "🏭 Sector Risk Assessment":
    
    st.markdown("## 🏭 **SECTOR RISK ASSESSMENT**")
    
    if len(sector_analysis) > 0:
        
        # Metriche settoriali
        col1, col2, col3, col4 = st.columns(4)
        
        worst_sector = sector_analysis.iloc[0]
        best_sector = sector_analysis.iloc[-1]
        high_risk_sectors = len(sector_analysis[sector_analysis['failure_rate'] > critical_threshold])
        
        with col1:
            st.markdown(f"""
            <div class="critical-metric">
                <h3 class="metric-title">💥 HIGHEST THREAT</h3>
                <h2 class="critical-value">{worst_sector.name[:10]}...</h2>
                <p class="metric-subtitle">{worst_sector['failure_rate']:.1f}% failure rate</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="success-metric">
                <h3 class="metric-title">✅ SAFEST SECTOR</h3>
                <h2 class="metric-value">{best_sector.name[:10]}...</h2>
                <p class="metric-subtitle">{best_sector['failure_rate']:.1f}% failure rate</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="warning-metric">
                <h3 class="metric-title">🚨 HIGH RISK</h3>
                <h2 class="metric-value">{high_risk_sectors}</h2>
                <p class="metric-subtitle">Above {critical_threshold}% threshold</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_sectors = len(sector_analysis)
            st.markdown(f"""
            <div class="cyber-metric">
                <h3 class="metric-title">📊 TOTAL SECTORS</h3>
                <h2 class="metric-value">{total_sectors}</h2>
                <p class="metric-subtitle">Under surveillance</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Analisi dettagliata settori
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 **SECTOR THREAT RANKING**")
            
            fig = go.Figure()
            
            # Color coding per livello di rischio
            colors = []
            for rate in sector_analysis['failure_rate']:
                if rate > critical_threshold:
                    colors.append('#d13ce0')  # Critico
                elif rate > 1.0:
                    colors.append('#8e44ad')  # Warning
                else:
                    colors.append('#00ff9f')  # Safe
            
            fig.add_trace(go.Bar(
                y=sector_analysis.index,
                x=sector_analysis['failure_rate'],
                orientation='h',
                marker_color=colors,
                text=sector_analysis['failure_rate'].round(2),
                textposition='auto',
                marker_line=dict(color='#e0e0e0', width=1),
                hovertemplate="<b>%{y}</b><br>" +
                              "Failure Rate: %{x}%<br>" +
                              "Total: %{customdata[0]}<br>" +
                              "Terminated: %{customdata[1]}<br>" +
                              "<extra></extra>",
                customdata=sector_analysis[['total', 'liquidated']].values
            ))
            
            # Aggiungi linea soglia critica
            fig.add_vline(x=critical_threshold, line_dash="dash", line_color="#d13ce0",
                         annotation_text=f"CRITICAL THRESHOLD {critical_threshold}%",
                         annotation_font_color="#d13ce0")
            
            fig.update_layout(
                title=dict(text="Failure Rate by Sector", font=dict(color='#e0e0e0')),
                xaxis_title="Failure Rate %",
                yaxis_title="Sector",
                height=500,
                plot_bgcolor='rgba(15,15,16,0.8)',
                paper_bgcolor='rgba(15,15,16,0)',
                font=dict(color='#e0e0e0'),
                xaxis=dict(gridcolor='rgba(142, 68, 173, 0.2)'),
                yaxis=dict(gridcolor='rgba(142, 68, 173, 0.2)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 **DETAILED RISK ANALYSIS**")
            
            # Settori critici
            critical_sectors = sector_analysis[sector_analysis['failure_rate'] > critical_threshold]
            
            if len(critical_sectors) > 0:
                st.markdown(f"""
                <div class="cyber-analysis">
                    <h4 style="color: #d13ce0;">🔴 CRITICAL SECTORS (>{critical_threshold}%)</h4>
                """, unsafe_allow_html=True)
                
                for sector, data in critical_sectors.iterrows():
                    st.markdown(f"""
                    <div style="background: rgba(209, 60, 224, 0.1); padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border: 1px solid rgba(209, 60, 224, 0.3);">
                        <strong style="color: #d13ce0;">{sector}</strong><br>
                        <span style="color: #e0e0e0; font-family: 'Courier New';">
                            • Failures: {data['failure_rate']:.2f}%<br>
                            • Total: {data['total']} entities<br>
                            • Terminated: {data['liquidated']}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.success("✅ **No sectors in critical zone**")
            
            # Settori warning
            warning_sectors = sector_analysis[(sector_analysis['failure_rate'] > 1.0) & (sector_analysis['failure_rate'] <= critical_threshold)]
            
            if len(warning_sectors) > 0:
                st.markdown(f"""
                <div class="cyber-analysis">
                    <h4 style="color: #8e44ad;">⚠️ WARNING SECTORS (1-{critical_threshold}%)</h4>
                """, unsafe_allow_html=True)
                
                for sector, data in warning_sectors.head(3).iterrows():
                    st.markdown(f"""
                    <div style="background: rgba(142, 68, 173, 0.1); padding: 0.8rem; margin: 0.3rem 0; border-radius: 6px; border: 1px solid rgba(142, 68, 173, 0.3);">
                        <strong style="color: #8e44ad;">{sector}</strong><br>
                        <small style="color: #e0e0e0; font-family: 'Courier New';">
                            {data['failure_rate']:.2f}% failures ({data['liquidated']}/{data['total']})
                        </small>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        # Tabella dettagliata se richiesta
        if show_details:
            st.markdown("### 📋 **COMPLETE SECTOR MATRIX**")
            
            sector_display = sector_analysis.reset_index()
            sector_display.columns = ['Sector', 'Total Entities', 'Terminated', 'Failure Rate %']
            st.dataframe(sector_display, use_container_width=True)
    
    else:
        st.error("❌ **Sector data matrix unavailable**")

elif analysis_type == "📍 Geographic Threat Map":
    
    st.markdown("## 📍 **GEOGRAPHIC THREAT MAP**")
    
    if len(geo_analysis) > 0:
        
        # Metriche geografiche
        col1, col2, col3, col4 = st.columns(4)
        
        worst_province = geo_analysis.iloc[0]
        best_province = geo_analysis.iloc[-1]
        high_risk_provinces = len(geo_analysis[geo_analysis['failure_rate'] > critical_threshold])
        
        with col1:
            st.markdown(f"""
            <div class="critical-metric">
                <h3 class="metric-title">💥 DANGER ZONE</h3>
                <h2 class="critical-value">{worst_province.name}</h2>
                <p class="metric-subtitle">{worst_province['failure_rate']:.1f}% mortality</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="success-metric">
                <h3 class="metric-title">✅ SAFE ZONE</h3>
                <h2 class="metric-value">{best_province.name}</h2>
                <p class="metric-subtitle">{best_province['failure_rate']:.1f}% mortality</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="warning-metric">
                <h3 class="metric-title">🚨 HIGH RISK ZONES</h3>
                <h2 class="metric-value">{high_risk_provinces}</h2>
                <p class="metric-subtitle">Above {critical_threshold}% threshold</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_provinces = len(geo_analysis)
            st.markdown(f"""
            <div class="cyber-metric">
                <h3 class="metric-title">📊 MONITORED ZONES</h3>
                <h2 class="metric-value">{total_provinces}</h2>
                <p class="metric-subtitle">With >10 entities</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Analisi geografica dettagliata
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🗺️ **TOP 15 HIGH-RISK PROVINCES**")
            
            top_provinces = geo_analysis.head(15)
            
            fig = go.Figure()
            
            # Color coding geografico
            colors = []
            for rate in top_provinces['failure_rate']:
                if rate > critical_threshold:
                    colors.append('#d13ce0')
                elif rate > 1.5:
                    colors.append('#8e44ad')
                else:
                    colors.append('#00ff9f')
            
            fig.add_trace(go.Bar(
                y=top_provinces.index,
                x=top_provinces['failure_rate'],
                orientation='h',
                marker_color=colors,
                text=top_provinces['failure_rate'].round(2),
                textposition='auto',
                marker_line=dict(color='#e0e0e0', width=1),
                hovertemplate="<b>%{y}</b><br>" +
                              "Failure Rate: %{x}%<br>" +
                              "Total: %{customdata[0]}<br>" +
                              "Terminated: %{customdata[1]}<br>" +
                              "<extra></extra>",
                customdata=top_provinces[['total', 'liquidated']].values
            ))
            
            fig.add_vline(x=critical_threshold, line_dash="dash", line_color="#d13ce0",
                         annotation_text=f"CRITICAL THRESHOLD {critical_threshold}%",
                         annotation_font_color="#d13ce0")
            
            fig.update_layout(
                title=dict(text="Failure Rate by Province", font=dict(color='#e0e0e0')),
                xaxis_title="Failure Rate %",
                yaxis_title="Province",
                height=600,
                plot_bgcolor='rgba(15,15,16,0.8)',
                paper_bgcolor='rgba(15,15,16,0)',
                font=dict(color='#e0e0e0'),
                xaxis=dict(gridcolor='rgba(142, 68, 173, 0.2)'),
                yaxis=dict(gridcolor='rgba(142, 68, 173, 0.2)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 **TERRITORIAL ANALYSIS**")
            
            # Province critiche
            critical_provinces = geo_analysis[geo_analysis['failure_rate'] > critical_threshold]
            
            if len(critical_provinces) > 0:
                st.markdown(f"""
                <div class="cyber-analysis">
                    <h4 style="color: #d13ce0;">🔴 CRITICAL PROVINCES</h4>
                """, unsafe_allow_html=True)
                
                for province, data in critical_provinces.head(5).iterrows():
                    st.markdown(f"""
                    <div style="background: rgba(209, 60, 224, 0.1); padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border: 1px solid rgba(209, 60, 224, 0.3);">
                        <strong style="color: #d13ce0;">{province}</strong><br>
                        <span style="color: #e0e0e0; font-family: 'Courier New';">
                            • Failures: {data['failure_rate']:.2f}%<br>
                            • Total entities: {data['total']}<br>
                            • Terminated: {data['liquidated']}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.success("✅ **No provinces in critical zone**")
            
            # Analisi dimensionale
            st.markdown(f"""
            <div class="cyber-analysis">
                <h4 style="color: #00ff9f;">📊 ECOSYSTEM SIZE ANALYSIS</h4>
                <ul style="color: #e0e0e0; font-family: 'Courier New';">
                    <li>Large ecosystem (>100): {len(geo_analysis[geo_analysis['total'] > 100])}</li>
                    <li>Medium ecosystem (50-100): {len(geo_analysis[(geo_analysis['total'] >= 50) & (geo_analysis['total'] <= 100)])}</li>
                    <li>Small ecosystem (10-50): {len(geo_analysis[(geo_analysis['total'] >= 10) & (geo_analysis['total'] < 50)])}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Top province per volume
            top_volume = geo_analysis.nlargest(5, 'total')
            
            st.markdown(f"""
            <div class="cyber-analysis">
                <h4 style="color: #8e44ad;">🏆 TOP ECOSYSTEMS (Volume)</h4>
            """, unsafe_allow_html=True)
            
            for province, data in top_volume.iterrows():
                st.markdown(f"""
                <div style="background: rgba(142, 68, 173, 0.1); padding: 0.8rem; margin: 0.3rem 0; border-radius: 6px; border: 1px solid rgba(142, 68, 173, 0.3);">
                    <strong style="color: #8e44ad;">{province}</strong><br>
                    <small style="color: #e0e0e0; font-family: 'Courier New';">
                        {data['total']} entities • {data['failure_rate']:.1f}% failures
                    </small>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Tabella dettagliata se richiesta
        if show_details:
            st.markdown("### 📋 **COMPLETE PROVINCE MATRIX**")
            
            geo_display = geo_analysis.reset_index()
            geo_display.columns = ['Province', 'Total Entities', 'Terminated', 'Failure Rate %']
            st.dataframe(geo_display, use_container_width=True)
    
    else:
        st.error("❌ **Geographic data matrix unavailable**")

elif analysis_type == "📊 Timeline Analysis":
    
    st.markdown("## 📊 **TIMELINE ANALYSIS PROTOCOL**")
    
    if len(timeline_data) > 0:
        
        # Metriche temporali
        col1, col2, col3, col4 = st.columns(4)
        
        peak_year = timeline_data.loc[timeline_data['startups_founded'].idxmax(), 'year']
        peak_value = timeline_data['startups_founded'].max()
        current_value = timeline_data.iloc[-1]['startups_founded']
        decline = ((current_value - peak_value) / peak_value * 100) if peak_value > 0 else 0
        
        with col1:
            st.markdown(f"""
            <div class="success-metric">
                <h3 class="metric-title">📈 PEAK YEAR</h3>
                <h2 class="metric-value">{int(peak_year)}</h2>
                <p class="metric-subtitle">{peak_value} entities founded</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            metric_class = "critical-metric" if decline < -30 else "warning-metric" if decline < 0 else "success-metric"
            st.markdown(f"""
            <div class="{metric_class}">
                <h3 class="metric-title">📉 CURRENT STATUS</h3>
                <h2 class="{'critical-value' if decline < -30 else 'metric-value'}">{current_value}</h2>
                <p class="metric-subtitle">{decline:+.1f}% vs peak</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_growth = timeline_data['growth_rate'].mean()
            metric_class = "critical-metric" if avg_growth < -10 else "warning-metric" if avg_growth < 0 else "success-metric"
            st.markdown(f"""
            <div class="{metric_class}">
                <h3 class="metric-title">⚡ AVG GROWTH</h3>
                <h2 class="{'critical-value' if avg_growth < -10 else 'metric-value'}">{avg_growth:.1f}%</h2>
                <p class="metric-subtitle">Per quarter</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_founded = timeline_data['startups_founded'].sum()
            st.markdown(f"""
            <div class="cyber-metric">
                <h3 class="metric-title">🎯 TOTAL PERIOD</h3>
                <h2 class="metric-value">{total_founded}</h2>
                <p class="metric-subtitle">Entities founded</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Timeline principale
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📊 **TEMPORAL FORMATION MATRIX**")
            
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Entities Founded per Quarter', 'Growth Rate %'),
                vertical_spacing=0.1
            )
            
            # Startup founded
            fig.add_trace(
                go.Scatter(
                    x=timeline_data['year_quarter'],
                    y=timeline_data['startups_founded'],
                    mode='lines+markers',
                    name='Entities Founded',
                    line=dict(color='#00ff9f', width=3),
                    marker=dict(size=8, color='#00ff9f', line=dict(color='#e0e0e0', width=1))
                ),
                row=1, col=1
            )
            
            # Growth rate con color coding cyber
            colors = []
            for x in timeline_data['growth_rate'].fillna(0):
                if x < -20:
                    colors.append('#d13ce0')
                elif x < 0:
                    colors.append('#8e44ad')
                else:
                    colors.append('#00ff9f')
            
            fig.add_trace(
                go.Bar(
                    x=timeline_data['year_quarter'],
                    y=timeline_data['growth_rate'].fillna(0),
                    name='Growth Rate %',
                    marker_color=colors,
                    marker_line=dict(color='#e0e0e0', width=1)
                ),
                row=2, col=1
            )
            
            # Aggiungi annotazioni per eventi critici
            if peak_value > 0:
                peak_quarter = timeline_data.loc[timeline_data['startups_founded'].idxmax(), 'year_quarter']
                fig.add_annotation(
                    x=peak_quarter, y=peak_value,
                    text=f"PEAK<br>{peak_value} entities",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor="#00ff9f",
                    bgcolor="rgba(0, 255, 159, 0.8)",
                    bordercolor="#e0e0e0",
                    font=dict(color="#0f0f10", size=10),
                    row=1, col=1
                )
            
            fig.update_layout(
                height=600,
                showlegend=True,
                plot_bgcolor='rgba(15,15,16,0.8)',
                paper_bgcolor='rgba(15,15,16,0)',
                font=dict(color='#e0e0e0'),
                xaxis=dict(gridcolor='rgba(142, 68, 173, 0.2)'),
                yaxis=dict(gridcolor='rgba(142, 68, 173, 0.2)'),
                xaxis2=dict(gridcolor='rgba(142, 68, 173, 0.2)'),
                yaxis2=dict(gridcolor='rgba(142, 68, 173, 0.2)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 **TREND ANALYSIS**")
            
            # Calcola statistiche trend
            recent_data = timeline_data.tail(4)  # Ultimi 4 trimestri
            recent_avg = recent_data['startups_founded'].mean()
            historical_avg = timeline_data['startups_founded'].mean()
            trend_change = ((recent_avg - historical_avg) / historical_avg * 100) if historical_avg > 0 else 0
            
            st.markdown(f"""
            <div class="cyber-analysis">
                <h4 style="color: #00ff9f;">📊 TREND MATRIX</h4>
                <ul style="color: #e0e0e0; font-family: 'Courier New';">
                    <li>Historical avg: <strong style="color:#00ff9f;">{historical_avg:.0f}</strong></li>
                    <li>Recent avg: <strong style="color:#8e44ad;">{recent_avg:.0f}</strong></li>
                    <li>Trend change: <strong style="color:#d13ce0;">{trend_change:+.1f}%</strong></li>
                    <li>Volatility: <strong style="color:#e0e0e0;">{timeline_data['startups_founded'].std():.0f}</strong></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Analisi per anno
            yearly_data = timeline_data.groupby('year').agg({
                'startups_founded': 'sum',
                'growth_rate': 'mean'
            }).round(1)
            
            st.markdown("### 📅 **ANNUAL PERFORMANCE**")
            
            for year, data in yearly_data.iterrows():
                year_change = data['growth_rate']
                if pd.isna(year_change):
                    year_change = 0
                    
                color = "#d13ce0" if year_change < -10 else "#8e44ad" if year_change < 0 else "#00ff9f"
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); padding: 0.8rem; margin: 0.5rem 0; border-radius: 5px; border-left: 3px solid {color};">
                    <strong style="color: #e0e0e0; font-family: 'Courier New';">{int(year)}</strong>: {data['startups_founded']:.0f} entities<br>
                    <small style="color: {color}; font-family: 'Courier New';">Growth: {year_change:+.1f}%</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Dettagli timeline se richiesti
        if show_details:
            st.markdown("### 📋 **TIMELINE MATRIX DETAILS**")
            
            timeline_display = timeline_data.copy()
            timeline_display['growth_rate'] = timeline_display['growth_rate'].round(1)
            timeline_display.columns = ['Year', 'Quarter', 'Entities Founded', 'Failures', 'Year-Quarter', 'Growth %']
            
            st.dataframe(timeline_display, use_container_width=True)
    
    else:
        st.warning("⚠️ **Temporal data matrix unavailable**")

# ============================================================================
# CYBER FOOTER CON INSIGHTS CRITICI
# ============================================================================

st.markdown("---")

st.markdown(f"""
<div style='background: linear-gradient(135deg, rgba(15, 15, 16, 0.95) 0%, rgba(142, 68, 173, 0.2) 50%, rgba(15, 15, 16, 0.95) 100%); 
     padding: 3rem; border-radius: 25px; margin-top: 2rem; 
     box-shadow: 0 0 50px rgba(142, 68, 173, 0.3), inset 0 0 30px rgba(209, 60, 224, 0.1);
     border: 2px solid rgba(142, 68, 173, 0.5); backdrop-filter: blur(15px);'>
    <h3 class='neon-header' style='text-align: center; margin-bottom: 2rem; font-size: 1.8rem;'>🎯 CRITICAL MATRIX SUMMARY</h3>
    <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem;'>
        <div class="cyber-analysis">
            <h4 style='color: #d13ce0; font-family: Courier New;'>💀 MORTALITY MATRIX</h4>
            <ul style="color: #e0e0e0; font-family: 'Courier New'; line-height: 1.6;">
                <li>Failure rate: <strong style="color: #d13ce0;">{mortality_stats['mortality_rate']:.2f}%</strong></li>
                <li>Terminated: <strong style="color: #d13ce0;">{mortality_stats['liquidated_startups']}</strong></li>
                <li>Highest risk: <strong style="color: #8e44ad;">{sector_analysis.index[0] if len(sector_analysis) > 0 else 'N/A'}</strong></li>
                <li>Survival: <strong style="color: #00ff9f;">{100-mortality_stats['mortality_rate']:.1f}%</strong></li>
            </ul>
        </div>
        <div class="cyber-analysis">
            <h4 style='color: #00ff9f; font-family: Courier New;'>💸 FUNDING MATRIX</h4>
            <ul style="color: #e0e0e0; font-family: 'Courier New'; line-height: 1.6;">
                <li>Neural match: <strong style="color: #00ff9f;">{funding_stats['matching_rate']:.1f}%</strong></li>
                <li>Funded entities: <strong style="color: #8e44ad;">{funding_stats['funding_success_rate']:.1f}%</strong></li>
                <li>Average funding: <strong style="color: #d13ce0;">${funding_stats['avg_funding']:,.0f}</strong></li>
                <li>Mega funded: <strong style="color: #00ff9f;">{funding_stats['mega_funded']} entities</strong></li>
            </ul>
        </div>
        <div class="cyber-analysis">
            <h4 style='color: #8e44ad; font-family: Courier New;'>📊 ECOSYSTEM HEALTH</h4>
            <ul style="color: #e0e0e0; font-family: 'Courier New'; line-height: 1.6;">
                <li>Total entities RI: <strong style="color: #e0e0e0;">{mortality_stats['total_startups']:,}</strong></li>
                <li>Sectors analyzed: <strong style="color: #8e44ad;">{len(sector_analysis)}</strong></li>
                <li>Provinces monitored: <strong style="color: #8e44ad;">{len(geo_analysis)}</strong></li>
                <li>Neural matches: <strong style="color: #00ff9f;">{len(funding_df)}</strong></li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# CYBER TECHNICAL SPECS
# ============================================================================

st.markdown(f"""
<div class="cyber-analysis" style="margin-top: 2rem;">
    <h3 class="cyber-title">🔧 TECHNICAL SPECIFICATIONS</h3>
    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 1rem;'>
        <div>
            <h4 style="color: #00ff9f; font-family: 'Courier New';">📁 DATA SOURCES</h4>
            <ul style="color: #e0e0e0; font-family: 'Courier New';">
                <li><strong>clean_dataset.xlsx</strong>: {len(df_ri):,} entities from Registro Imprese</li>
                <li><strong>da vedere.xlsx</strong>: {len(df_cb):,} entities from Crunchbase</li>
                <li><strong>Prevalenza.xlsx</strong>: Classification legends</li>
            </ul>
        </div>
        <div>
            <h4 style="color: #8e44ad; font-family: 'Courier New';">🔬 METHODOLOGY</h4>
            <ul style="color: #e0e0e0; font-family: 'Courier New';">
                <li>Neural matching: Name-based similarity algorithm</li>
                <li>Mortality analysis: Status field evaluation</li>
                <li>Timeline: Registration date temporal analysis</li>
                <li>Funding: Total USD amount processing</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# CYBER SIGNATURE
# ============================================================================

st.markdown(f"""
---
<div style='text-align: center; padding: 1rem; font-family: Courier New;'>
    <p style='color: #8e44ad; margin: 0;'>
        🚀 <strong>STARTUP REALITY MATRIX</strong> • 
        ⚡ <strong>Midnight Pulse Edition</strong> • 
        🔬 <strong>Neural Network Analysis</strong>
    </p>
    <p style='color: #e0e0e0; margin: 0.5rem 0; font-size: 0.9rem;'>
        Powered by Streamlit • Plotly • Pandas • Real Data Matrix
    </p>
    <p style='color: #d13ce0; margin: 0; font-size: 0.8rem;'>
        Matrix Status: <span style="color: #00ff9f;">ONLINE</span> • 
        Last Update: <span style="color: #8e44ad;">Real-time</span> • 
        Security: <span style="color: #00ff9f;">ENCRYPTED</span>
    </p>
</div>
""", unsafe_allow_html=True)
