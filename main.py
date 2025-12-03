import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap

st.set_page_config(page_title="Défi 2 - Territoires et vulnérabilités", layout="wide")

# --- Données ---
gdf = gpd.read_file("Data_input/communes-1000m.geojson")  # adapte le chemin

# --- Sidebar / Filtres ---
st.sidebar.title("Filtres")

# 🔹 Choix Région
region_list = sorted(gdf["region"].dropna().unique())
region = st.sidebar.selectbox("Choisir une région", region_list)
df_region = gdf[gdf["region"] == region]

# 🔹 Choix Département
departement_list = sorted(df_region["departement"].dropna().unique())
departement = st.sidebar.selectbox("Choisir un département", ["Tous"] + departement_list)
if departement != "Tous":
    df_dep = df_region[df_region["departement"] == departement]
else:
    df_dep = df_region

# 🔹 Choix Zone
zone_list = sorted(df_dep["nom"].dropna().unique())
zone = st.sidebar.selectbox("Choisir une zone", zone_list)
df_selected = df_dep[df_dep["nom"] == zone]

# --- CARTE ---
st.title("Défi 2 - Territoires et vulnérabilités")
m = leafmap.Map(center=[47, -2], zoom=7)

# Couche complète (selon filtre Région/Département)
m.add_gdf(df_dep, layer_name="Communes filtrées")

# Couche sélectionnée
if not df_selected.empty:
    m.add_gdf(df_selected, layer_name="Zone sélectionnée",
              style={"color": "blue", "weight": 3})

m.to_streamlit(height=600)

# --- INFOS COMPLEMENTAIRES ---
st.subheader("Informations sur la zone sélectionnée")
if not df_selected.empty:
    row = df_selected.iloc[0]
    st.metric("Nom", row["nom"])
    st.metric("Département", row["departement"])
    st.metric("EPCI", row["epci"])
else:
    st.info("Aucune donnée pour la zone sélectionnée.")

st.sidebar.markdown("## 👥 Équipe Défi 2 : Impact sur les populations vulnérables des îlots de chaleur")

st.sidebar.markdown("""
### Notre équipe
- **Pauline Allée** – Data / Climat  
- **Denis Vannier** – Cartographe  
- **Antoine Roy** – Data Scientist  
- **Adrien Salem-Sermanet** – Data Scientist
- **Marc Le Moing** – Data Scientist                    

📍 *Hackathon Météo France 2025*
""")