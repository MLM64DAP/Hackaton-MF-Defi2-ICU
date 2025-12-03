import streamlit as st

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
tabs = st.tabs(["Notre projet", "Carte interactive"])


# --- Onglet 1 : Contexte scientifique ---
with tabs[0]:
    st.title("🌡️ ClimAtlas Vulnérabilités")

    st.markdown("""
    ## 🎯 Objectif du projet

    Identifier le niveau d'exposition aux **risques climatiques** — vagues de chaleur, nuits tropicales et vagues de nuits tropicales — 
    pour les **populations vulnérables**, aux horizons **2030** et **2050** (méthodologie TRACC). 🌍

    ---
                
    🔗 [Voir le code source sur GitHub](https://github.com/royantoine/impact-chaleur-future-population) 💻

    ---
                
    ## 1. Contexte : hausse des températures & croissance des populations âgées 🌡️👵👴

    La France connaît déjà une multiplication des épisodes de fortes chaleurs à travers son territoire.  
    Les projections climatiques régionales montrent que cette tendance va s’accentuer d’ici 2030 puis 2050, avec :  

    - 🔥 Davantage de **jours à plus de 35°C**, dangereux pour la santé  
    - 🌙 Des **nuits tropicales (>20°C)**, empêchant la récupération physiologique  
    - 🌞 Des **vagues de chaleur** de plus longue durée  
    - 🏙️ Une intensification du phénomène d’**îlots de chaleur urbains** dans les villes  

    Ces épisodes affectent particulièrement les **personnes vulnérables**, notamment les **personnes âgées**, surtout si elles vivent seules, en milieu urbain dense ou dans des zones précaires.  
    La population française vieillissante fera que la proportion de personnes de 65 ans et plus sera nettement plus élevée en 2050.  
    L’intersection entre population plus âgée et exposition croissante aux chaleurs extrêmes constitue un enjeu majeur de santé publique et d’aménagement du territoire.

    ### 1.1 Evolution de la population +65 ans 📈
    """)
    st.image("image_2.webp", width=600)
    st.caption("Source : [INED - Vieillissement de la population](https://www.ined.fr/fr/tout-savoir-population/memos-demo/focus/vieillissement-de-la-population-accelere-en-france-et-dans-la-plupart-des-pays-developpes/)")

    st.markdown("""
    ### 1.2 Vagues de chaleur en France 🌞
    """)
    st.image("image_1.webp", width=600)
    st.caption("Source : [DRIAS - Vagues de chaleur](https://www.drias-climat.fr/accompagnement/sections/417)")

    st.markdown("""
    ## 2. Problématique & proposition de valeur ❓💡

    ### Problématique
    Comment visualiser rapidement, à **échelle spatiale fine**, l’évolution du risque de fortes chaleurs pour les personnes âgées sur l’ensemble du territoire entre aujourd’hui et 2050 ?

    ### Proposition de valeur
    Fournir une plateforme simple, interactive et autoportante permettant de croiser **données climatiques** et **données démographiques** pour repérer les territoires — jusqu’à l’échelle des quartiers — où la vulnérabilité thermique des personnes âgées va le plus augmenter.  

    L’outil vise à transmettre en quelques secondes une information précise, actionnable et territorialisée, utile aux **collectivités**, **urbanistes**, **acteurs sanitaires** et **décideurs publics**.
    """)

    # --- 3. La solution ---
    st.markdown("## 3. La solution 🛠️")

    st.subheader("3.1 Visualisation de la solution 🖼️")
    st.image(
        "image.webp",
        caption="Schéma illustrant la solution ClimAtlas Vulnérabilités",
        width=600
    )

    st.markdown("""
    ### 3.2 Description générale
    L’application Streamlit comprend :  

    - 🗺️ Une **carte interactive** permettant :
      - de naviguer dans le territoire à différentes échelles (commune / EPCI / département / région)
      - d’afficher le croisement d’un indicateur représentatif de l’aléa de forte chaleur et de la démographie des populations âgées, aujourd’hui et à l’horizon 2050 (+2.7°C)
    - 📖 Une **page de documentation intégrée**, rendant la solution accessible et compréhensible sans expertise préalable  

    ➡️ Application en ligne : [ClimAtlas Vulnérabilités](https://hackaton-mf-defi2-icu-xpkqbvnjcbszzp2yzgavl3.streamlit.app/)

    ### 3.3 Usage des données
    **Données climatiques — Météo-France / CPRCM** 🌡️  
    - Modèle : CNRM-AROME46t1, 2,5 km de résolution  
    - Forçage : CNRM-ESM2-1, scénario SSP3-7.0  
    - Périodes TRACC :
      - **baseline** : 2015–2034, pivot 2025
      - **+2.7°C** : 2068–2087, pivot 2078  

    **Indicateurs climatiques** :  
    - Pire cas annuel sur 20 ans pour le nombre de jours et nuits consécutifs en vague de chaleur (min > 20°C et max > 35°C)  
    - Autres indicateurs non intégrés faute de temps :  
      - Nombre de nuits tropicales (min > 20°C)  
      - Nombre de jours en vague de nuits tropicales  
      - Nombre de jours avec vagues de chaleur (max > 35°C)  

    **Données démographiques — INSEE** 👥  
    - Projections 2018–2070 par département  
    - Données carroyées (1 km²) pour la distribution spatiale fine  
    - Variables : population totale, personnes âgées  

    ### 3.4 Méthode de construction de la solution 🧩
    - Extraction et traitement des données CPRCM  
    - Calcul des indicateurs de fortes chaleurs annuels  
    - Agrégation par maximum sur 20 ans  
    - Construction d’un dataset consolidé par scénario (actuel et +2.7°C)  
    - Préparation des données démographiques  
    - Croisement climat × démographie pour calculer un risque combiné  
    - Création de l’application Streamlit avec visualisation interactive  

    ---
    """)


# --- Onglet 2 : Carte interactive ---
with tabs[1]:
    st.header("Carte interactive des indicateurs de chaleur")

    # ⚠️ Warning pour le temps de chargement
    st.warning("⚠️ Le temps de chargement de la carte peut être un peu long en fonction de votre connexion et du filtrage choisi.")


    st.markdown("### 🔎 Carte dynamique hébergée sur le site de l'équipe")
    st.markdown("*(Développée via Mapbox )*")

    # ---- Affichage de la carte via IFRAME ----
    st.components.v1.iframe(
        src="https://leplan.studio/wip/test2_hackathon_MF/",
        height=800,
        scrolling=True
    )





