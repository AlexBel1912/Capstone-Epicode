# ULTIMATE STARTUP INTELLIGENCE PLATFORM - VERSIONE STABILE
# ===========================================================
# Funziona anche con UN SOLO FILE CSV da Registro Imprese
# Supporta: Calcolo KPI, AI, Visualizzazioni, Alert, Benchmark
# ===========================================================

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import plotly.express as px

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Ultimate Startup Dashboard", layout="wide")
st.title("🚀 Ultimate Startup Intelligence Platform")

# --- FUNZIONE: Caricamento File CSV ---
st.sidebar.header("Carica il file CSV da Registro Imprese")
file = st.sidebar.file_uploader("File Registro Startup", type=["csv", "xlsx"])

# --- Mappa sigle province -> regioni (semplificata)
province_to_region = {
    'RM': 'Lazio', 'MI': 'Lombardia', 'TO': 'Piemonte', 'FI': 'Toscana',
    'NA': 'Campania', 'BO': 'Emilia-Romagna', 'VE': 'Veneto', 'BA': 'Puglia',
    'GE': 'Liguria', 'PV': 'Lombardia', 'PD': 'Veneto', 'MO': 'Emilia-Romagna'
    # aggiungine altre se necessario
}

if file:
    # --- Lettura Dati ---
    try:
        df = pd.read_csv(file, sep=';', encoding='utf-8')
    except Exception:
        file.seek(0)
        df = pd.read_csv(file, sep=',', encoding='latin1')

    st.subheader("📊 Anteprima Dati Originali")
    st.dataframe(df.head())

    # --- Pulizia nomi colonne ---
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace("-", "_")

    # --- Rinomina colonne per adattare al modello
    df = df.rename(columns={
        'classe_di_produzione_ultimo_anno_(1)': 'classe_fatturato',
        'classe_di_addetti_ultimo_anno_(2)': 'classe_addetti',
        'data_iscrizione_al_registro_imprese': 'data_costituzione',
        'settore': 'settore',
        'denominazione': 'denominazione'
    })

    df['regione'] = df['pv'].map(province_to_region)

    required_cols = ['denominazione', 'regione', 'settore', 'data_costituzione', 'classe_fatturato', 'classe_addetti']
    if not all(col in df.columns for col in required_cols):
        st.error("❌ Il file non contiene tutte le colonne richieste:")
        st.write(required_cols)
        st.stop()

    # --- Feature Engineering ---
    df['età'] = pd.to_datetime('today').year - pd.to_datetime(df['data_costituzione'], errors='coerce').dt.year

    mapping_fatturato = {
        'Fino a 10.000': 5_000,
        '10.000 - 50.000': 30_000,
        '50.000 - 100.000': 75_000,
        '100.000 - 500.000': 300_000,
        '500.000 - 1.000.000': 750_000,
        'Oltre 1.000.000': 1_500_000
    }
    df['fatturato_stimato'] = df['classe_fatturato'].map(mapping_fatturato)

    mapping_addetti = {
        '0': 0,
        '1-2': 1.5,
        '3-5': 4,
        '6-10': 8,
        '11-20': 15,
        '21-50': 35,
        'Oltre 50': 60
    }
    df['addetti_stimati'] = df['classe_addetti'].map(mapping_addetti)

    df['produttività'] = df['fatturato_stimato'] / df['addetti_stimati'].replace(0, np.nan)
    df['capital_efficiency'] = df['produttività'] / df['età']

    # --- Calcolo AI Success Score ---
    df_model = df[['età', 'fatturato_stimato', 'addetti_stimati']].dropna()
    df_model = df_model[df_model['addetti_stimati'] > 0]
    df_model['success'] = (df_model['fatturato_stimato'] > 100000).astype(int)

    X = df_model[['età', 'addetti_stimati']]
    y = df_model['success']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    df['ai_success_probability'] = model.predict_proba(df[['età', 'addetti_stimati']].fillna(0))[:, 1]

    # --- VISUALIZZAZIONE KPI ---
    st.subheader("📈 Indicatori Generali")
    col1, col2, col3 = st.columns(3)
    col1.metric("Numero di Startup", f"{df.shape[0]:,}")
    col2.metric("Fatturato Totale Stimato", f"€ {df['fatturato_stimato'].sum():,.0f}")
    col3.metric("Età Media Startup", f"{df['età'].mean():.1f} anni")

    # --- GRAFICO: Success Probability ---
    st.subheader("🔮 Probabilità di Successo (AI Prediction)")
    fig = px.histogram(df, x='ai_success_probability', nbins=20, title="Distribuzione delle Probabilità di Successo")
    st.plotly_chart(fig, use_container_width=True)

    # --- TABELLA FINALE ---
    st.subheader("📋 Dataset con Indicatori e Score")
    st.dataframe(df[['denominazione', 'regione', 'settore', 'età', 'fatturato_stimato', 'addetti_stimati', 'produttività', 'capital_efficiency', 'ai_success_probability']].round(2))

else:
    st.info("📥 Carica un file CSV da analizzare")
