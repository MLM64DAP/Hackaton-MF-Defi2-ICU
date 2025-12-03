import streamlit as st
import json
import leafmap.foliumap as leafmap

st.set_page_config(page_title="Défi 2 - Territoires et vulnérabilités", layout="wide")

# --- Données ---
with open("Data_input/communes-1000m.geojson", "r", encoding="utf-8") as f:
    gjson = json.load(f)

features = gjson["features"]

# Conversion en dictionnaire → liste simple pour manipuler les attributs
records = [feat["properties"] for feat in features]

# --- Extraire les valeurs uniques ---
regions = sorted({r["region"] for r in records if r.get("region")})
departements_by_region = {}
for r in regions:
    departements_by_region[r] = sorted(
        {rec["departement"] for rec in records if rec["region"] == r and rec.get("departement")}
    )

# --- Sidebar / Filtres ---
st.sidebar.title("Filtres")

# 🔹 Région
region = st.sidebar.selectbox("Choisir une région", regions)

# 🔹 Départements dépendants
deps = ["Tous"] + departements_by_region[region]
departement = st.sidebar.selectbox("Choisir un département", deps)

# Filtrage records
if departement != "Tous":
    filtered = [rec for rec in records if rec["region"] == region and rec["departement"] == departement]
else:
    filtered = [rec for rec in records if rec["region"] == region]

# 🔹 Zones
zone_list = sorted({rec["nom"] for rec in filtered})
zone = st.sidebar.selectbox("Choisir une zone", zone_list)

selected = next((rec for rec in filtered if rec["nom"] == zone), None)

# --- CARTE ---
st.title("Défi 2 - Territoires et vulnérabilités")

m = leafmap.Map(center=[47, -2], zoom=7)

# Couche filtrée
m.add_geojson(gjson, layer_name="Communes filtrées")

# Couche sélectionnée (on filtre le GeoJSON)
if selected:
    selected_geojson = {
        "type": "FeatureCollection",
        "features": [
            feat for feat in gjson["features"]
            if feat["properties"]["nom"] == selected["nom"]
        ]
    }
    m.add_geojson(
        selected_geojson,
        layer_name="Zone sélectionnée",
        style={"color": "blue", "weight": 3}
    )

m.to_streamlit(height=600)

# --- Infos ---
st.subheader("Informations sur la zone sélectionnée")

if selected:
    st.metric("Nom", selected["nom"])
    st.metric("Département", selected["departement"])
    st.metric("EPCI", selected.get("epci", "N/A"))
else:
    st.info("Aucune donnée pour la zone sélectionnée.")

# --- Sidebar équipe ---
st.sidebar.markdown("## 👥 Équipe Défi 2 : Impact des îlots de chaleur")

st.sidebar.markdown("""
### Notre équipe
- **Pauline Allée** – Data / Climat  
- **Denis Vannier** – Cartographe  
- **Antoine Roy** – Data Scientist  
- **Adrien Salem-Sermanet** – Data Scientist  
- **Marc Le Moing** – Data Scientist  

📍 *Hackathon Météo France 2025*
""")
