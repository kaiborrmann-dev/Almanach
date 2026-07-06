import streamlit as st

# --- LOGIK-MODUL: BACKEND ---

class FallacyChecker:
    @staticmethod
    def detect(observed):
        errors = []
        if len(observed) < 2:
            errors.append("Modul 14: Abstraktions-Falle (Datenbasis zu gering).")
        return errors

class BethTableauEngine:
    @staticmethod
    def check_consistency(requirement, observed):
        # Logik-Kern: Beth-Kalkül (Falsifizierung)
        req_set = set(requirement.replace(" ", "").split("∧"))
        obs_set = set(observed)
        return req_set.issubset(obs_set)

# --- KONFIGURATION: TAXONOMIE ---

TAXONOMY = [
    {"id": "T1", "name": "Der kalkulierte Erbe", "req": "P_Besitz∧P_Konservierung"},
    {"id": "T2", "name": "Der Markt-Akteur", "req": "P_Besitz∧P_Expansion"},
    {"id": "T3", "name": "Der strategische Investor", "req": "P_Besitz∧P_Langzeit-Kalkül"},
    # ... (T4-T15 analog einfügen)
]

# --- FRONTEND: STREAMLIT APP ---

st.set_page_config(page_title="Soziologische Maschine", layout="wide")
st.title("Soziologische Maschine: Demystifizierungs-Apparat")

# Input-Bereich
hexis = st.text_input("Hexis (Beobachtete Haltung):", placeholder="z.B. konzentriert, fokussiert")
doxa = st.text_input("Doxa (Beobachteter Kontext):", placeholder="z.B. Finanzmarkt-Volatilität")
observed_preds = st.multiselect("Prädikate (Daten-Eingabe):", ["P_Besitz", "P_Expansion", "P_Bildung", "P_Relation"])

if st.button("Analysieren"):
    st.subheader("Analyse-Ergebnisse")
    
    # 1. Analyse der Merkmale
    best_match = None
    fallacies = FallacyChecker.detect(observed_preds)
    
    if fallacies:
        for f in fallacies: st.warning(f)
    
    # 2. Visualisierung: Prädikaten-Baum
    cols = st.columns(5)
    for idx, item in enumerate(TAXONOMY):
        is_consistent = BethTableauEngine.check_consistency(item["req"], observed_preds)
        
        with cols[idx % 5]:
            if is_consistent:
                st.markdown(f"**<span style='color:black'>{item['id']}: {item['name']}</span>**", unsafe_allow_html=True)
                best_match = item
            else:
                st.markdown(f"<span style='color:grey'>{item['id']}: {item['name']}</span>", unsafe_allow_html=True)

    # 3. Finales Urteil
    if best_match:
        st.success(f"Logische Einordnung: {best_match['id']}")
        st.write(f"**Kurze Begründung:** Die Zuordnung zu {best_match['id']} erfolgt durch Erfüllung des Bedeutungseinschlusses ({best_match['req']}).")
    else:
        st.error("Keine logische Konsistenz mit den 15 Archetypen gefunden. Tableau geschlossen.")
