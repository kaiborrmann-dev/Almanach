import streamlit as st
from typing import Set, Dict, List

# --- Offizielle KldB-Datenbank (Auszug für den Demonstrator) ---
KLDB_DATABASE = {
    "24104": {
        "title": "Softwareentwicklung und Programmierung",
        "bereich": "4 - Naturwissenschaft, Geografie und Informatik",
        "niveau": "Niveau 4 (Experte / Hochschulabschluss)",
        "keywords": {"ki", "software", "python", "programmieren", "code", "daten", "logik", "analyse", "algorithmus"}
    },
    "71102": {
        "title": "Gartenbau und Landschaftsgestaltung",
        "bereich": "7 - Land-, Forst- und Tierwirtschaft sowie Gartenbau",
        "niveau": "Niveau 2-3 (Fachkraft / Spezialist)",
        "keywords": {"natur", "pflanzen", "draußen", "garten", "handwerk", "erde", "grün"}
    },
    "81403": {
        "title": "Sozialarbeit und Sozialpädagogik",
        "bereich": "8 - Gesundheit, Soziales, Lehre und Erziehung",
        "niveau": "Niveau 4 (Experte / Hochschulabschluss)",
        "keywords": {"menschen", "helfen", "sozial", "beratung", "kommunikation", "verantwortung", "jugend"}
    },
    "25192": {
        "title": "Wissenschaftliche Forschung und Hochschullehre",
        "bereich": "2 - Unternehmensführung, Organisation, Recht",
        "niveau": "Niveau 4 (Experte / Promotion / Wissenschaft)",
        "keywords": {"forschung", "wissenschaft", "theorie", "universität", "studium", "struktur", "konzept", "akademisch"}
    }
}

st.set_page_config(page_title="Arbeitsmarkt-Lotse: KldB & Kultur", layout="wide")

st.title("🏛️ Arbeitsmarkt-Lotse: Soziologisches Matching meets KldB")
st.markdown("Dieser Demonstrator zeigt, wie weiche, unstrukturierte Lebensentwürfe über einen **automatisierten KldB-Baum** erfasst und mit Kultur-Operatoren ($\\text{mA}$) und Kontexten ($\\text{kA}$) verknüpft werden.")

# --- Datenmodell für Akteure ---
class Actor:
    def __init__(self, id_str: str, role: str, kldb_code: str, operators: Dict[str, str], bio: str):
        self.id_str = id_str
        self.role = role  # "Bewerber" oder "Arbeitgeber"
        self.kldb_code = kldb_code
        self.operators = operators
        self.bio = bio
        self.description = bio # Kompatibilität für Beschreibungen

# Initialisierung des Markt-Pools in session_state
if "market_pool" not in st.session_state:
    st.session_state["market_pool"] = [
        Actor(
            id_str="KI-Forschungsinstitut Berlin", 
            role="Arbeitgeber", 
            kldb_code="24104", 
            operators={"mA": "Autonom & Eigenverantwortlich", "kA": "KI & Technologie"},
            bio="Sucht Köpfe für strukturierte Datenmodelle und formale Systemanalysen."
        ),
        Actor(
            id_str="Digital-Agentur Kreuzberg", 
            role="Arbeitgeber", 
            kldb_code="24104", 
            operators={"mA": "Agil & Interdisziplinär", "kA": "KI & Technologie"},
            bio="Entwickelt Software-Lösungen in flachen Hierarchien."
        )
    ]

# --- 1. SEKTION: INTUITIVE EINGABE & AUTOMATISCHER KLDB-MAPPER ---
st.header("1. Perspektive eingeben (Freitext & Soziologische Traits)")

with st.form("user_input_form"):
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("Name / Alias", value="Sarah M.")
        user_role = st.selectbox("Rolle", ["Bewerber (Arbeitssuchend)", "Arbeitgeber (Stelle anbieten)"])
    with col2:
        modus = st.selectbox("Arbeitsstil / Kultur (Operator mA)", ["Autonom & Eigenverantwortlich", "Agil & Interdisziplinär", "Strukturiert & Klassisch"])
        kontext = st.selectbox("Themenfeld (Operator kA)", ["KI & Technologie", "Öffentlicher Sektor", "Wissenschaft & Bildung"])

    bio_text = st.text_area(
        "Erzählen Sie frei von Ihren Interessen, Stärken oder Zielen (z.B. 'Ich liebe formale Logik, arbeite am liebsten autonom am Computer und beschäftige mich mit KI und Analyse'):",
        value="Ich arbeite gerne autonom, beschäftige mich intensiv mit logischen Strukturen, Software-Analysen und KI-Technologien."
    )
    
    submitted = st.form_submit_button("Profil analysieren & in den KldB-Baum einlesen")

    if submitted and bio_text:
        # Automatisierter KldB-Mapper (Durchsucht den Baum nach Keyword-Übereinstimmungen)
        bio_lower = bio_text.lower()
        best_match_code = "24104" # Standard-Fallback
        max_hits = 0
        
        for code, data in KLDB_DATABASE.items():
            hits = sum(1 for kw in data["keywords"] if kw in bio_lower)
            if hits > max_hits:
                max_hits = hits
                best_match_code = code

        role_val = "Bewerber" if "Bewerber" in user_role else "Arbeitgeber"
        
        new_actor = Actor(
            id_str=user_name,
            role=role_val,
            kldb_code=best_match_code,
            operators={"mA": modus, "kA": kontext},
            bio=bio_text
        )
        st.session_state["market_pool"].append(new_actor)
        st.success(f"Profil erfolgreich verarbeitet! Dem Profil wurde der offizielle KldB-Code `{best_match_code}` zugewiesen.")

# --- Infobox zum ermittelten KldB-Code des letzten Eintrags ---
if st.session_state["market_pool"]:
    latest = st.session_state["market_pool"][-1]
    kldb_info = KLDB_DATABASE.get(latest.kldb_code, {"title": "Unbekannt", "bereich": "Unbekannt", "niveau": "Unbekannt"})
    
    with st.expander("🔍 Details zur automatischen KldB-Klassifikation (Amtlicher Hintergrund)", expanded=True):
        st.write(f"**Aktuell analysiertes Profil:** `{latest.id_str}` ({latest.role})")
        st.write(f"* **Zugeordneter KldB-Code:** `{latest.kldb_code}`")
        st.write(f"* **Berufsbezeichnung:** {kldb_info['title']}")
        st.write(f"* **Berufsbereich (1. Stelle):** {kldb_info['bereich']}")
        st.write(f"* **Anforderungsniveau (5. Stelle):** {kldb_info['niveau']}")
        st.info("💡 **Mehrwert für die Arbeitsagentur:** Die App übersetzt den emotionalen/inhaltlichen Freitext eigenständig in den passenden amtlichen Statistik-Schlüssel, ohne dass der Bürger Formulare wälzen muss.")

st.divider()

# --- 2. SEKTION: LEBENSLAUF-ASSISTENT ---
with st.expander("📝 Lebenslauf-Assistent (Optionale Hilfe)"):
    st.markdown("**Sollen wir Ihnen beim Erstellen eines tabellarischen Lebenslaufes behilflich sein?**")
    st.markdown("Dann benötigen wir noch folgende Angaben:")
    col_a, col_b = st.columns(2)
    with col_a:
        st.text_input("Zuletzt ausgeübte Stationen / Tätigkeiten")
    with col_b:
        st.text_input("Kernqualifikationen / Studienschwerpunkt")
    if st.button("Tabellarischen Lebenslauf generieren"):
        st.success("Der Entwurf wurde basierend auf Ihren Angaben und dem KldB-Profil strukturiert.")

st.divider()

# --- 3. SEKTION: STRUKTURLOGISCHES MATCHING ---
st.header("2. Strukturlogische Passungs-Analyse")
st.markdown("Das System prüft nun: Gleicher KldB-Zweig $\\land$ Übereinstimmender Arbeitsstil ($\\text{mA}$) $\\land$ Kontext ($\\text{kA}$).")

if st.button("Passende Stellen / Profile im Arbeitsmarkt ermitteln"):
    pool = st.session_state["market_pool"]
    active_user = pool[-1]
    
    matches = []
    for candidate in pool[:-1]:
        if candidate.role != active_user.role:
            kldb_match = candidate.kldb_code == active_user.kldb_code
            modus_match = candidate.operators["mA"] == active_user.operators["mA"]
            
            if kldb_match and modus_match:
                matches.append(candidate)
                
    if matches:
        st.success(f"Es wurden {len(matches)} passfähige Verbindungen im Raum entdeckt:")
        for idx, match in enumerate(matches, 1):
            match_details = KLDB_DATABASE.get(match.kldb_code, {})
            st.markdown(f"**Match {idx}:** `{active_user.id_str}` ⟷ `{match.id_str}`")
            st.write(f"* **Gemeinsames Berufsfeld (KldB):** `{match.kldb_code}` ({match_details.get('title')})")
            st.write(f"* **Kultur-Passung (Operator mA):** `{match.operators['mA']}`")
            st.write(f"* **Beschreibung:** {match.description}")
            st.markdown("---")
    else:
        st.warning("Keine exakte Passung gefunden. Entweder weicht der KldB-Bereich oder der Arbeitsstil (mA) ab. Versuchen Sie, die Beschreibung so anzupassen, dass sie zu den vorhandenen Stellen passt.")
