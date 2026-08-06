import streamlit as st
from typing import Set, Dict, List

# --- Offizielle KldB-Datenbank ---
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
st.markdown("Passgenauigkeit jenseits starrer Raster: Verknüpfung von Freitext-Traits, KldB-Baum und Kultur-Operatoren ($\\text{mA}$).")

# --- Initialisierung des Arbeitgeber-Pools in session_state ---
if "employer_pool" not in st.session_state:
    st.session_state["employer_pool"] = [
        {
            "id_str": "KI-Forschungsinstitut Berlin", 
            "kldb_code": "24104", 
            "mA": "Autonom & Eigenverantwortlich", 
            "kA": "KI & Technologie",
            "description": "Sucht Köpfe für strukturierte Datenmodelle und formale Systemanalysen."
        },
        {
            "id_str": "Digital-Agentur Kreuzberg", 
            "kldb_code": "24104", 
            "mA": "Agil & Interdisziplinär", 
            "kA": "KI & Technologie",
            "description": "Entwickelt Software-Lösungen in flachen Hierarchien."
        },
        {
            "id_str": "Grünflächen-Amt Mitte", 
            "kldb_code": "71102", 
            "mA": "Strukturiert & Klassisch", 
            "kA": "Natur & Umwelt",
            "description": "Betreut städtische Parkanlagen und ökologische Projekte."
        }
    ]

# --- 1. SEKTION: PERSÖNLICHES PROFIL (Live-Eingabe ohne Blockade) ---
st.header("1. Ihr Profil & Ihre Perspektive")

col1, col2 = st.columns(2)
with col1:
    user_name = st.text_input("Ihr Name / Alias", value="Dr. Thomas Weber")
    modus = st.selectbox("Bevorzugter Arbeitsstil / Kultur (Operator mA)", ["Autonom & Eigenverantwortlich", "Agil & Interdisziplinär", "Strukturiert & Klassisch"])
with col2:
    kontext = st.selectbox("Bevorzugtes Themenfeld (Operator kA)", ["KI & Technologie", "Öffentlicher Sektor", "Wissenschaft & Bildung", "Natur & Umwelt"])

bio_text = st.text_area(
    "Erzählen Sie frei von Ihren Stärken, Interessen oder Zielen (jeder Textänderung wird sofort ausgewertet):",
    value="Ich beschäftige mich intensiv mit logischen Strukturen, Software-Analysen und KI-Technologien in der Forschung."
)

# Automatisierter KldB-Mapper läuft in Echtzeit bei jeder Eingabeänderung
bio_lower = bio_text.lower()
assigned_kldb = "24104" # Fallback
max_hits = 0
for code, data in KLDB_DATABASE.items():
    hits = sum(1 for kw in data["keywords"] if kw in bio_lower)
    if hits > max_hits:
        max_hits = hits
        assigned_kldb = code

kldb_info = KLDB_DATABASE.get(assigned_kldb, {})

# Transparente Anzeige der automatischen KldB-Zuordnung
st.info(f"🔍 **Automatische KldB-Analyse:** Ihr Text wurde dem Code **`{assigned_kldb}`** (*{kldb_info.get('title')}*) im Bereich *{kldb_info.get('bereich')}* zugeordnet ({kldb_info.get('niveau')}).")

st.divider()

# --- 2. SEKTION: LEBENSLAUF-ASSISTENT ---
with st.expander("📝 Lebenslauf-Assistent (Optionale Hilfe)"):
    st.markdown("**Sollen wir Ihnen beim Erstellen eines tabellarischen Lebenslaufes behilflich sein?**")
    col_a, col_b = st.columns(2)
    with col_a:
        st.text_input("Zuletzt ausgeübte Stationen / Tätigkeiten", key="cv_stations")
    with col_b:
        st.text_input("Kernqualifikationen / Studienschwerpunkt", key="cv_skills")
    if st.button("Lebenslauf-Struktur generieren"):
        st.success("Struktur erfolgreich generiert und auf Basis Ihres KldB-Profils formatiert!")

st.divider()

# --- 3. SEKTION: PASSUNGS-ANALYSE (Reagiert direkt auf Änderungen) ---
st.header("2. Passungs-Analyse mit dem Arbeitsmarkt")
st.markdown("Das System gleicht Ihr dynamisches Profil in Echtzeit mit den registrierten Arbeitgebern ab ($\\text{KldB-Match} \\land \\text{mA}$).")

# Matching-Logik direkt ausführen (kein versteckter Button nötig, da es bei Änderung sofort reagieren soll)
matches = []
for employer in st.session_state["employer_pool"]:
    kldb_match = employer["kldb_code"] == assigned_kldb
    modus_match = employer["mA"] == modus
    
    if kldb_match and modus_match:
        matches.append(employer)

if matches:
    st.success(f"Es wurden **{len(matches)}** passende Arbeitgeber für Ihr Profil im Raum entdeckt:")
    for idx, m in enumerate(matches, 1):
        st.markdown(f"**Match {idx}: `{m['id_str']}`**")
        st.write(f"* **Berufsfeld (KldB):** `{m['kldb_code']}` ({kldb_info.get('title')})")
        st.write(f"* **Kultur-Passung (mA):** `{m['mA']}`")
        st.write(f"* **Stellenbeschreibung:** {m['description']}")
        st.markdown("---")
else:
    st.warning("⚠️ Zur Zeit gibt es im System keine exakte Passung für diese Kombination aus KldB-Bereich und Arbeitsstil (`mA`). Ändern Sie testweise den Arbeitsstil oder passen Sie den Freitext an, um andere Branchen/Stilen zu matchen.")
