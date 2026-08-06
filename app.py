import streamlit as st
from typing import Set, Dict, List

# --- Konfiguration & KldB-Daten (Auszug) ---
# In einer echten App würde hier die KldB-Datenbank (CSV/API) liegen.
KLDB_DATABASE = {
    "24103": {"name": "Informatik / KI-Entwicklung", "keywords": {"ki", "software", "python", "algorithmus", "logik", "daten"}},
    "71101": {"name": "Gartenbau / Landschaftspflege", "keywords": {"natur", "pflanzen", "draußen", "handwerk", "erde"}},
    "81101": {"name": "Soziale Arbeit / Pädagogik", "keywords": {"menschen", "helfen", "sozial", "kommunikation", "verantwortung"}}
}

st.set_page_config(page_title="Arbeitsmarkt-Lotse", layout="wide")

st.title("🏛️ Arbeitsmarkt-Lotse: Soziologisches Matching & KldB")
st.markdown("Wir verbinden individuelle Lebensentwürfe mit der offiziellen Klassifikation der Berufe (KldB).")

# --- Datenmodell für den Demonstrator ---
class Actor:
    def __init__(self, id_str: str, role: str, kldb_code: str, preds: Set[str], operators: Dict[str, str], bio: str):
        self.id_str = id_str
        self.role = role
        self.kldb_code = kldb_code # KldB 5-Steller
        self.predicates = preds
        self.operators = operators
        self.bio = bio

# Simulation eines Markt-Pools
if "market_pool" not in st.session_state:
    st.session_state["market_pool"] = [
        Actor("KI-Forschungszentrum", "Arbeitgeber", "24103", {"ki", "logik"}, {"mA": "Autonom & Eigenverantwortlich", "kA": "KI & Technologie"}, "Forschungszentrum für formale Logik."),
        Actor("Stadtgarten GmbH", "Arbeitgeber", "71101", {"natur", "handwerk"}, {"mA": "Strukturiert & Klassisch", "kA": "Natur & Umwelt"}, "Landschaftspflege und Stadterneuerung.")
    ]

# --- 1. Sektion: Intuitive Erfassung ---
st.header("1. Erzählen Sie uns von Ihrer Perspektive")
with st.form("user_profile_form"):
    name = st.text_input("Name")
    bio = st.text_area("Was motiviert Sie? Wie arbeiten Sie am liebsten? (z.B. 'Ich liebe Logik und Autonomie bei der Arbeit am Computer')")
    
    col1, col2 = st.columns(2)
    modus = col1.selectbox("Wie arbeiten Sie am liebsten?", ["Autonom & Eigenverantwortlich", "Strukturiert & Klassisch", "Sozial & Kommunikativ"])
    kontext = col2.selectbox("Welches Umfeld suchen Sie?", ["KI & Technologie", "Natur & Umwelt", "Soziales & Bildung"])
    
    submitted = st.form_submit_button("Profil analysieren")

    if submitted:
        # Mini-Logik zur KldB-Inferenz
        bio_lower = bio.lower()
        matched_kldb = "24103" # Fallback/Standard
        for code, info in KLDB_DATABASE.items():
            if any(k in bio_lower for k in info["keywords"]):
                matched_kldb = code
                break
        
        preds = set(w for w in bio_lower.split() if len(w) > 3)
        new_user = Actor(name, "Bewerber", matched_kldb, preds, {"mA": modus, "kA": kontext}, bio)
        st.session_state["market_pool"].append(new_user)
        st.success(f"Analyse abgeschlossen! Ihr Berufsprofil wurde gemappt auf KldB-Code: {matched_kldb}")

# --- 2. Sektion: CV-Assistent ---
with st.expander("📝 Benötigen Sie Hilfe beim tabellarischen Lebenslauf?"):
    st.write("Wir helfen Ihnen, Ihre soziologischen Traits in formale KldB-Strukturen zu übersetzen.")
    st.text_input("Zuletzt ausgeübte Tätigkeit:")
    st.text_input("Höchster Abschluss:")
    if st.button("Lebenslauf-Entwurf generieren"):
        st.info("Funktion in Arbeit: Ihr Entwurf wird basierend auf Ihren Daten erstellt.")

# --- 3. Sektion: Matching-Engine ---
st.divider()
st.header("2. Passungs-Analyse")
if st.button("Potenzielle Arbeitgeber finden"):
    pool = st.session_state["market_pool"]
    user = pool[-1] # Letzter Eintrag
    
    matches = []
    for entity in pool[:-1]: # Suche in Arbeitgebern
        if entity.role == "Arbeitgeber":
            # Matching-Kriterien:
            # 1. KldB-Nähe (Job-Familie)
            # 2. Modus-Passung (mA)
            # 3. Kontext-Passung (kA)
            match_kldb = entity.kldb_code == user.kldb_code
            match_modus = entity.operators["mA"] == user.operators["mA"]
            
            if match_kldb and match_modus:
                matches.append(entity)
    
    if matches:
        st.subheader("Ihre optimalen Match-Partner:")
        for m in matches:
            st.success(f"**Match:** {m.id_str} (KldB: {m.kldb_code})")
            st.write(f"Stil: {m.operators['mA']} | Feld: {m.operators['kA']}")
    else:
        st.warning("Keine exakte Übereinstimmung in den Stil-Parametern gefunden. Prüfen Sie, ob Ihre Arbeitsweise mit den Unternehmen korrespondiert.")
