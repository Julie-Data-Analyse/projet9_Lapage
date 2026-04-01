import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# # ============================================
# # Chargement des données
# # ============================================

@st.cache_data 

def load_data():
    base_path = Path(__file__).resolve().parents[2]
    file_path = base_path / "data" / "processed" / "df_lapage.csv"  
    df = pd.read_csv(file_path, sep=';')  
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# # ============================================
# # COULEURS
# # ============================================

palette = {
    "0": "#e95c6d",
    "1": "#2f3a4a",
    "2": "#ffa600"
}

# # ============================================
# # HEADER
# # ============================================
st.set_page_config(page_title="Marketing", layout="wide")
st.sidebar.header("Marketing")

KPI1, KPI2, KPI3, KPI4 = st.columns(4)

st.title(":material/menu_book: Dashboard Lapage")
st.markdown("Analyse des ventes de la Librairie Lapage")

# # ============================================
# # SIDEBAR - FILTRES
# # ============================================
st.sidebar.header("Filtres")

#  Filtre de catégories
st.sidebar.subheader("Filtre par catégorie")
categories = ["Toutes"] + sorted([str(c) for c in df['categ'].unique()])
selected_categ = st.sidebar.selectbox("Choisir une catégorie", categories)


#  Filtre de dates
st.sidebar.subheader("Sélection de la période")
min_date = df['date'].min().date()
max_date = df['date'].max().date()

periode = st.sidebar.date_input(
    "Choisir la période",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

#  Utilisation des filtres
df_filtered = df.copy()

# Filtre Date
if isinstance(periode, tuple) and len(periode) == 2:
    start_date, end_date = periode
    df_filtered = df_filtered[
        (df_filtered['date'].dt.date >= start_date) & 
        (df_filtered['date'].dt.date <= end_date)
    ]

# Filtre Catégorie
if selected_categ != "Toutes":
    df_filtered = df_filtered[df_filtered['categ'] == int(selected_categ)]

# Filtre segments B2B et B2C
# if selected_segment != "Toutes":
#     df_filtered = df_filtered[df_filtered['categ'] == int(selected_categ)]

# # ============================================
# # SECTION 1 - KPIs
# # ============================================
st.header("Indicateurs clés")

if df_filtered.empty:
    st.warning("Aucune donnée disponible pour cette sélection.")
else:
    KPI1, KPI2, KPI3 = st.columns(3)

with KPI1:
    categorie0 = df_filtered('categ')['price'].sum()
    st.metric(label="CA Catégorie 0", value=f"{categorie0:,.0f} €".replace(',', ' '))

with KPI2:
    categorie1 = df_filtered('categ')['price'].sum()
    st.metric(label="CA Catégorie 1", value=f"{categorie1:,.0f} €".replace(',', ' '))


with KPI3:
    categorie2 = df_filtered('categ')['price'].sum()
    st.metric(label="CA Catégorie 2", value=f"{categorie2:,.0f} €".replace(',', ' '))

# # ============================================
# # SECTION 2 - GRAPHIQUE CA
# # ============================================
st.header("Evolution du CA")

df_chrono = df_filtered.resample('MS', on='date')['price'].sum().reset_index()

fig = px.line(
    df_chrono, 
    x='date', 
    y='price', 
    title=f"CA Mensuel - Catégorie: {selected_categ}",
    labels={'price': 'Chiffre d\'Affaires (€)', 'date': 'Mois'},
    markers=True
)

st.plotly_chart(fig, width="content")


# # ============================================
# # SECONDE PAGE - PROFILS CLIENTS
# # ============================================
st.header("Evolution du CA")
# Ajout d'une analyse par catégorie si "Toutes" est sélectionné
if selected_categ == "Toutes":
    st.header("Répartition par Catégorie")
    df_pie = df.groupby('categ')['price'].sum().reset_index()
    fig_pie = px.pie(df_pie, values='price', names='categ', title="Part du CA par catégorie")
    st.plotly_chart(fig_pie, width="Stretch")