# Analisi Ecosistema Startup Italia (2020–2024)

**Capstone finale del corso Data Analyst Epicode**  
_A cura di Alexandra Belacurencu_

---

## 🚀 Obiettivo  
Analizzare la crescita, le caratteristiche e i finanziamenti delle startup innovative italiane nate tra il 2020 e il 2024, con l'obiettivo di individuare pattern, concentrazioni regionali e gap strutturali dell'ecosistema.

---

## 📈 Dataset Overview
* **+10.000** startup analizzate (fondate dal 2020 al 2024)  
* **2 fonti dati integrate**: Registro Imprese, VeM  
* **15+ variabili chiave**: settore, capitale, addetti, fondazione, status, finanziamenti  
* **Copertura nazionale**: 20 regioni, 107 province, oltre 6.000 comuni

---

## 🛠️ Pipeline Tecnologica
* **Data Extraction**: Power Query, csv scaricato dal sito ufficiale di registro imprese
* **Data Processing**: Pandas, Regex, Join logici
* **Analysis**: KPI sintetici, Geographic clustering, Indici di diversità  
* **Visualization**: Power BI (report interattivo), Plotly
* **Deployment**: Git + GitHub LFS, Documentazione integrata

---

## 📊 Report Power BI  
**File:** `Analisi ecosistema StartUp Italia 2020–2024 - Final Version.pbix`  
Contenuti principali:
- **Overview temporale**: trend annuali e mensili  
- **Distribuzione geografica**: mappa interattiva + dettaglio per comune  
- **Profili & caratteristiche**: diversità, capitale, forza lavoro  
- **Settori**: classificazione ATECO + dinamiche settoriali  
- **Investimenti**: analisi Venture Capital + Deal Flow  
- **Indicatori ESG & readiness**: vocazione sociale, high-tech, capital efficiency

---

## 🗂️ Dataset principali  
- `fact_startup_registry.csv` – Anagrafica startup da Registro Imprese  
- `Fact_VEM_Investments.csv` – Operazioni di investimento (fonte VeM)  
- `georef-italy-comune.csv` – Latitudine/longitudine comuni italiani  
- `Dim_Geography.csv`, `Dim_Sector.csv`, `Dim_Investor.csv` – Tabelle dimensionali  
