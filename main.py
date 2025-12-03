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
tabs = st.tabs(["Contexte scientifique", "Carte interactive", "Pour aller plus loin"])


# --- Onglet 1 : Contexte scientifique ---
with tabs[0]:
    st.title("🌡️ ClimAtlas Vulnérabilités : Impact des îlots de chaleur sur les populations sensibles")

    st.markdown("""
    ## 🎯 Objectif du projet
    Identifier le niveau d'exposition aux **risques climatiques** — vagues de chaleur, nuits tropicales et vagues de nuits tropicales — 
    pour les **populations vulnérables**, en particulier les personnes âgées, aux horizons **2030** et **2050** (méthodologie TRACC).

    🔗 [Voir le code source sur GitHub](https://github.com/royantoine/impact-chaleur-future-population)

    ---  

    ## 1. Contexte : hausse des températures et vieillissement de la population
    La France connaît déjà une multiplication des épisodes de fortes chaleurs. Les projections climatiques régionales montrent que cette tendance va s'accentuer d'ici 2030 puis 2050, avec :

    - Plus de **jours à >35°C**, dangereux pour la santé  
    - Des **nuits tropicales (>20°C)**, limitant la récupération physiologique  
    - Des **vagues de chaleur** plus longues  
    - Une intensification des **îlots de chaleur urbains**  

    Les populations **âgées**, **isolées** ou **précaires** sont les plus vulnérables.  
    La proportion de personnes de 65 ans et plus va fortement augmenter d'ici 2050, ce qui accentue les enjeux de santé publique et d'aménagement du territoire.

    ### 1.1 Visualisation de la population +65 ans
    """)
    st.image("image_2.webp", width=600)
    st.caption("Source : [INED - Vieillissement de la population](https://www.ined.fr/fr/tout-savoir-population/memos-demo/focus/vieillissement-de-la-population-accelere-en-france-et-dans-la-plupart-des-pays-developpes/)")

    st.markdown("""
    ### 1.2 Vagues de chaleur en France
    """)
    st.image("image_1.webp", width=600)
    st.caption("Source : [DRIAS - Vagues de chaleur](https://www.drias-climat.fr/accompagnement/sections/417)")
    st.markdown("""
    ---  

    ## 2. Problématique & proposition de valeur
    ### Problématique
    Comment visualiser rapidement, à **échelle spatiale fine**, l’évolution du risque de fortes chaleurs pour les personnes âgées sur l’ensemble du territoire jusqu’en 2050 ?

    ### Proposition de valeur
    Fournir une plateforme **interactive**, simple et autoportante, permettant de croiser **données climatiques** et **données démographiques** afin de repérer les territoires — jusqu’aux quartiers — où la vulnérabilité thermique va le plus augmenter.  
    Utile pour les **collectivités**, **urbanistes**, **acteurs sanitaires** et **décideurs publics**.

    ---  

    ## 3. La solution
    ### 3.1 Visualisation de la solution
    """)
    st.image("image.webp", caption="Schéma illustrant la solution ClimAtlas Vulnérabilités", width=600)

    st.markdown("""
    ### 3.2 Description générale
    L’application Streamlit comprend :  

    - Une **carte interactive** pour naviguer à différentes échelles (commune / EPCI / département / région) et croiser un indicateur de chaleur avec la démographie des populations âgées (actuel et +2.7°C)  
    - Une **documentation intégrée**, pour rendre la solution accessible sans expertise préalable  

    ➡️ Application en ligne : [ClimAtlas Vulnérabilités](https://hackaton-mf-defi2-icu-xpkqbvnjcbszzp2yzgavl3.streamlit.app/)

    ### 3.3 Données utilisées
    **Climatiques — CPRCM / Météo-France**  
    - Modèle : CNRM-AROME46t1, 2,5 km  
    - Forçage : CNRM-ESM2-1, SSP3-7.0  
    - Périodes TRACC : baseline (2015–2034, pivot 2025) et +2.7°C (2068–2087, pivot 2078)  

    **Démographiques — INSEE**  
    - Projections 2018–2070 par département  
    - Carroyage 1 km² pour distribution spatiale fine  
    - Variables : population totale, personnes âgées  

    ### 3.4 Méthodologie
    - Extraction et traitement des données climatiques  
    - Calcul des indicateurs de vagues de chaleur annuelles (pire cas sur 20 ans)  
    - Descente d’échelle et préparation des données démographiques  
    - Croisement climat × démographie pour calculer un risque combiné  
    - Déploiement via une **application Streamlit** avec visualisation interactive  

    ---  

    ## 4. Impact et usages
    - Identifier les **territoires prioritaires** exposés  
    - Observer l’évolution de l’exposition des populations âgées  
    - Soutenir : urbanisme climatique, politiques de prévention, PCAET, diagnostics territoriaux  

    ---  

    ## 5. Ressources
    - **Application en ligne** : [ClimAtlas Vulnérabilités](https://hackaton-mf-defi2-icu-xpkqbvnjcbszzp2yzgavl3.streamlit.app/)  
    - **Dépôt GitHub** : [impact-chaleur-future-population](https://github.com/royantoine/impact-chaleur-future-population)  
    Contient : notebooks climat, code démographique, application Streamlit, README méthodologie  

    ## 6. Perspectives futures
    - Intégration de données fines sur vulnérabilité (IRIS, WorldPop, précarité, isolement)  
    - Études sur les îlots de chaleur urbains vs zones rurales  
    - Indicateurs climatiques supplémentaires (+4°C, seuils régionalisés)
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

