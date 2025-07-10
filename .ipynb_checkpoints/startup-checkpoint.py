import streamlit as st
import pandas as pd
import plotly.express as px


# Layout pagina
st.set_page_config(page_title="Analisi Startup Italiane", layout="wide")
st.title("Dashboard Startup Italiane (2020-2024)")

# Carica i dati
@st.cache_data
def load_data():
    df = pd.read_csv("startup_pulito_powerbi.csv", parse_dates=["data_iscrizione_startup"])
    return df

df = load_data()

# Filtri laterali
with st.sidebar:
    st.header("Filtri")
    regioni = st.multiselect("Seleziona Regione", options=df["regione"].dropna().unique(), default=None)
    settore = st.multiselect("Seleziona Settore", options=df["settore"].dropna().unique(), default=None)
    anno_range = st.slider("Anno di Iscrizione", 2020, 2024, (2020, 2024))

# Applica filtri
filtro = (df["data_iscrizione_startup"].dt.year.between(anno_range[0], anno_range[1]))
if regioni:
    filtro &= df["regione"].isin(regioni)
if settore:
    filtro &= df["settore"].isin(settore)

df_filt = df[filtro]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Numero Startup", f"{df_filt.shape[0]:,}")
col2.metric("Regioni Coinvolte", df_filt["regione"].nunique())
col3.metric("Settori Unici", df_filt["settore"].nunique())

# Grafico per anno
st.subheader("Andamento delle Startup per Anno")
df_filt["anno"] = df_filt["data_iscrizione_startup"].dt.year
df_year = df_filt.groupby("anno").size().reset_index(name="Numero Startup")
fig_anno = px.bar(df_year, x="anno", y="Numero Startup", text_auto=True)
st.plotly_chart(fig_anno, use_container_width=True)

# Mappa geolocalizzazione
st.subheader("Distribuzione Geografica per Regione")
df_geo = df_filt["regione"].value_counts().reset_index()
df_geo.columns = ["Regione", "Numero Startup"]
fig_map = px.choropleth(df_geo,
                        locations="Regione",
                        locationmode="country names",
                        color="Numero Startup",
                        scope="europe",
                        title="Startup per Regione")
st.plotly_chart(fig_map, use_container_width=True)

# Grafico settori
st.subheader("Distribuzione per Settore Economico")
df_sett = df_filt["settore"].value_counts().nlargest(10).reset_index()
df_sett.columns = ["Settore", "Numero Startup"]
fig_sett = px.bar(df_sett, x="Settore", y="Numero Startup", text_auto=True)
st.plotly_chart(fig_sett, use_container_width=True)

# Tabella
st.subheader("Anteprima Dati Filtrati")
st.dataframe(df_filt.head(50))
