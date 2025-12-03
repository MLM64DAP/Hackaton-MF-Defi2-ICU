import streamlit as st
import json
import leafmap.foliumap as leafmap

st.set_page_config(page_title="Défi 2 - Territoires et vulnérabilités", layout="wide")

# --- Sidebar équipe (toujours visible) ---
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

# --- Onglets ---
tabs = st.tabs(["Contexte scientifique", "Carte interactive"])

# --- Onglet 1 : Contexte scientifique ---
with tabs[0]:
    st.title("Impact des îlots de chaleur et du réchauffement climatique sur les populations sensibles")
    
    st.markdown("""
    ## 🎯 Objectif du projet

    Identifier le niveau d'exposition aux **risques climatiques** — vagues de chaleur, nuits tropicales et vagues de nuits tropicales — auxquels seront confrontées les **populations vulnérables** selon leur localisation, aux horizons **2030** et **2050** (méthodologie TRACC).

    ---

    ## 🧠 Problématique

    Le réchauffement climatique augmente la fréquence et l’intensité :

    - des **jours > 35°C**, dangereux pour la santé (déshydratation, surmortalité)  
    - des **nuits tropicales (>20°C)**, limitant la récupération physiologique  
    - des **vagues de chaleur** (≥ 3 jours consécutifs très chauds)  
    - des **vagues de nuits tropicales** (≥ 3 nuits consécutives >20°C)  

    Les populations **âgées**, **précaires** ou **isolées** sont les plus vulnérables. Ce projet vise à mesurer cet impact à une échelle fine pour aider les collectivités à anticiper.

    ---

    ## 🧬 Approche adoptée

    1. **Indicateurs climatiques** issus du modèle CPRCM (CNRM-AROME 2,5 km), forcé par CNRM-ESM2-1 pour le scénario SSP3-7.0  
    2. Calcul des indicateurs sur 20 ans pour chaque scénario, puis prise du **maximum annuel** :  
    - `n_tropical_nights_min20`  
    - `n_heatwaves_days_min20_max35`  
    - `n_heatwaves_days_min20`  
    - `n_heatwaves_days_max35`  
    3. **Croisement** avec les données INSEE : population totale, ménages, pauvreté, part +65 ans…  
    4. **Projection démographique** Insee alignée sur les scénarios TRACC (2030 et 2050).  
    5. Intégration dans une **plateforme interactive Streamlit** pour permettre :
    - la sélection dynamique d’un territoire (commune / EPCI / département / région)  
    - la visualisation cartographique  
    - l’analyse de la vulnérabilité climatique et démographique  

    ---

    ## 🛰️ Données utilisées

    ### 🌡️ Données climatiques  
    Projection régionale CPRCM (CNRM-AROME46t1, 2,5 km) selon 3 périodes :

    | Période | Scénario TRACC | Année pivot | Fenêtre temporelle |
    |--------|----------------|-------------|---------------------|
    | Aujourd’hui | Baseline | 2025 | 2015–2034 |
    | +2°C | TRACC 2030 | 2052 | 2042–2061 |
    | +2.7°C | TRACC 2050 | 2078 | 2068–2087 |

    ---

    ## 📊 Indicateurs retenus

    Pour chaque scénario, 4 indicateurs majeurs :

    - **Nombre annuel de nuits tropicales**  
    - **Nombre annuel de jours en vague de chaleur (min >20°C & max >35°C)**  
    - **Nombre de jours en vague de nuits tropicales**  
    - **Nombre de jours en vague de chaleur v0 (max >35°C)**  

    ⚠️ Les valeurs correspondent au **pire cas possible** sur 20 ans (maximum annuel).

    ---

    ## 🏛️ Usages attendus

    - aide à la **planification territoriale** et à la politique de la ville  
    - identification des **quartiers prioritaires** les plus exposés  
    - appui à la lutte contre les **îlots de chaleur urbains**  
    - préparation des plans d’adaptation locaux (PCAET, diagnostics CRTE…)

    ---
    """)


# --- Onglet 2 : Carte interactive ---
with tabs[1]:
    st.header("Carte interactive des indicateurs de chaleur")

    # --- Données ---
    with open("Data_input/communes-1000m.geojson", "r", encoding="utf-8") as f:
        gjson = json.load(f)

    features = gjson["features"]
    records = [feat["properties"] for feat in features]

    # --- Sidebar filtres (Région/Département/Zone) ---
    st.sidebar.title("Filtres carte")

    regions = sorted({r["region"] for r in records if r.get("region")})
    region = st.sidebar.selectbox("Choisir une région", regions)

    departements_by_region = {}
    for r in regions:
        departements_by_region[r] = sorted(
            {rec["departement"] for rec in records if rec["region"] == r and rec.get("departement")}
        )

    deps = ["Tous"] + departements_by_region[region]
    departement = st.sidebar.selectbox("Choisir un département", deps)

    if departement != "Tous":
        filtered = [rec for rec in records if rec["region"] == region and rec["departement"] == departement]
    else:
        filtered = [rec for rec in records if rec["region"] == region]

    zone_list = sorted({rec["nom"] for rec in filtered})
    zone = st.sidebar.selectbox("Choisir une zone", zone_list)

    selected = next((rec for rec in filtered if rec["nom"] == zone), None)

    # --- Carte ---
    m = leafmap.Map(center=[47, -2], zoom=7)
    m.add_geojson(gjson, layer_name="Communes filtrées")

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

    # --- Infos zone ---
    st.subheader("Informations sur la zone sélectionnée")
    if selected:
        st.metric("Nom", selected["nom"])
        st.metric("Département", selected["departement"])
        st.metric("EPCI", selected.get("epci", "N/A"))
    else:
        st.info("Aucune donnée pour la zone sélectionnée.")
