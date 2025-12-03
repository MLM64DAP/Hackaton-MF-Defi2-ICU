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
    ### Qu'est-ce qu'un îlot de chaleur ?
    Les **îlots de chaleur urbains** sont des zones où la température est significativement plus élevée que dans les zones rurales environnantes, principalement à cause de l’urbanisation, du béton et du manque de végétation.

    ### Populations sensibles
    - Personnes âgées  
    - Enfants  
    - Personnes souffrant de maladies chroniques  
    - Ménages à faibles revenus  

    ### Indicateurs étudiés
    - **Jours à plus de 35°C**  
    - **Nuits tropicales**  
    - **Populations âgées projetées en 2070**  
    - **Indice combiné de sensibilité**

    ### Conséquences
    - Risques accrus de **coup de chaleur et maladies cardiovasculaires**  
    - Augmentation de la **mortalité et morbidité**  
    - Accentuation des **inégalités sociales et territoriales**
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
