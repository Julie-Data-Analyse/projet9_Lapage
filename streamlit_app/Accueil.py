import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Accueil", layout="wide")

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
st.set_page_config(
    page_title="Dashboard Lapage", 
    page_icon="menu_book",
    
)

st.title("Dashboard Lapage")

st.write('Bienvenue sur le dashboard de la librairie Lapage !')