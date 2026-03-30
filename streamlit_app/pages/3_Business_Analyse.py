import streamlit as st
import pandas as pd
import plotly.express as px



# # ============================================
# # Chargement des données
# # ============================================

@st.cache_data 

def load_data():
    df = pd.read_csv(r'data/processed/df_b2c.csv',sep=';')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# # ============================================
# # HEADER
# # ============================================
st.set_page_config(
    page_title="Business Analyse")
st.sidebar.header("Business Analyse")

st.title("Dashboard Lapage")
st.markdown("Résumé statistique")

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

# # ============================================
# # SECTION 1 - KPIs
# # ============================================
st.header("Indicateurs clés")

if df_filtered.empty:
    st.warning("Aucune donnée disponible pour cette sélection.")
else:
    KPI1, KPI2, KPI3, KPI4 = st.columns(4)

with KPI1:
    ca_total = df_filtered['price'].sum()
    st.metric(label="CA Total", value=f"{ca_total:,.0f} €".replace(',', ' '))

with KPI2:
    st.metric(label="Nb Ventes", value=len(df_filtered))

with KPI3:
    nb_clients = df_filtered['client_id'].nunique() if 'client_id' in df.columns else "N/A"
    st.metric(label="Clients Uniques", value=nb_clients)
with KPI4:
    if 'session_id' in df.columns:
        panier = ca_total / df_filtered['session_id'].nunique()
        st.metric(label="Panier Moyen", value=f"{panier:.2f} €")
    else:
        st.metric(label="Prix Moyen / Article", value=f"{df_filtered['price'].mean():.2f} €")

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

st.plotly_chart(fig, use_container_width=True)


# # ============================================
# # SECONDE PAGE - PROFILS CLIENTS
# # ============================================
st.header("Evolution du CA")
# Ajout d'une analyse par catégorie si "Toutes" est sélectionné
if selected_categ == "Toutes":
    st.header("Répartition par Catégorie")
    df_pie = df.groupby('categ')['price'].sum().reset_index()
    fig_pie = px.pie(df_pie, values='price', names='categ', title="Part du CA par catégorie")
    st.plotly_chart(fig_pie, use_container_width="Stretch")