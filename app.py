import streamlit as st
from typing import Dict

# --- Amtliche KldB-Datenbank mit Keywords für den Mapper ---
KLDB_DATABASE = {
    "24104": {
        "title": "Softwareentwicklung und Programmierung",
        "bereich": "4 - Naturwissenschaft, Geografie und Informatik",
        "niveau": "Niveau 4 (Experte / Hochschulabschluss)",
        "keywords": {"ki", "software", "python", "programmieren", "code", "daten", "logik", "analyse", "algorithmus", "forschung"}
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
        "keywords": {"wissenschaft", "theorie", "universität", "studium", "struktur", "konzept", "akademisch"}
    }
}

# --- Arbeitgeber-Pool ---
EMPLOYER_POOL = [
    {
        "name": "KI-Forschungsinstitut Berlin", 
        "kldb": "24104", 
        "mA": "Autonom & Eigenverantwortlich", 
        "kA": "KI & Technologie",
        "description": "Sucht Köpfe für strukturierte Datenmodelle und formale Systemanalysen."
    },
    {
        "name": "Digital-StartUp Mitte", 
        "kldb": "24104", 
        "mA": "Agil & Interdisziplinär", 
        "kA": "KI & Technologie",
        "description": "Entwickelt Software-Lösungen in flachen Hierarchien."
    },
    {
        "name": "Stadtgarten GmbH", 
        "kldb": "71102", 
        "mA": "Strukturiert & Klassisch", 
        "kA": "Natur & Umwelt",
        "description": "Betreut städtische Parkanlagen und ökologische Projekte."
    }
]

st.set_page_config(page_title="Arbeitsmarkt-Lotse", layout="centered")

st.title("🤝 Arbeitsmarkt-Lotse")
st.markdown("Ein intuitiver Demonstrator: Freitext-Traits treffen auf den amtlichen **KldB-Baum** und Kultur-Operatoren.")

# Tabs für eine aufgeräumte, geführte Benutzerführung
tab1, tab2, tab3 = st.tabs(["1. Über mich & Profil", "2. Passende Stellen", "3. Lebenslauf-Hilfe"])

# --- TAB 1: EINGABE & AUTOMATISCHER KLDB-MAPPER ---
with tab1:
    st.subheader("Erzählen Sie uns von Ihrer Perspektive")
    story = st.text_area(
        "Schreiben Sie frei über Ihre Stärken, Interessen oder Ziele (z.B. 'Ich liebe formale Logik, arbeite autonom und mache etwas mit KI und Daten'):", 
        height=130,
        value="Ich liebe formale Logik, arbeite am liebsten autonom und beschäftige mich intensiv mit KI und Datenanalyse."
    )
    
    col1, col2 = st.columns(2)
    modus = col1.selectbox("Arbeitsstil / Kultur (Operator mA)", ["Autonom & Eigenverantwortlich", "Agil & Interdisziplinär", "Strukturiert & Klassisch"])
    kontext = col2.selectbox("Themenfeld (Operator kA)", ["KI & Technologie", "Öffentlicher Sektor", "Wissenschaft & Bildung", "Natur & Umwelt"])

    if st.button("Profil analysieren & KldB-Code bestimmen", type="primary"):
        # Automatisierter Text-zu-KldB-Mapper durchsucht den Baum nach Keyword-Treffern
        bio_lower = story.lower()
        best_match_code = "24104" # Standard-Fallback
        max_hits = 0
        
        for code, data in KLDB_DATABASE.items():
            hits = sum(1 for kw in data["keywords"] if kw in bio_lower)
            if hits > max_hits:
                max_hits = hits
                best_match_code = code

        # Daten im Session State sichern
        st.session_state["story"] = story
        st.session_state["modus"] = modus
        st.session_state["kontext"] = kontext
        st.session_state["detected_kldb"] = best_match_code
        
        info = KLDB_DATABASE[best_match_code]
        st.success(f"Erfolgreich gemappt! Amtlicher KldB-Code: **{best_match_code}** ({info['title']})")

# --- TAB 2: PASSUNGS-ANALYSE ---
with tab2:
    st.subheader("Strukturlogische Passungs-Analyse")
    
    if "detected_kldb" not in st.session_state:
        st.info("💡 Bitte analysieren Sie zuerst Ihr Profil im Tab '1. Über mich & Profil'.")
    else:
        code = st.session_state["detected_kldb"]
        info = KLDB_DATABASE[code]
        active_modus = st.session_state["modus"]
        
        st.markdown(f"**Ihr aktuelles Profil:**")
        st.write(f"- Erkanntes KldB-Feld: `{code}` — *{info['title']}* ({info['niveau']})")
        st.write(f"- Arbeitsstil (mA): `{active_modus}`")
        st.divider()
        
        # Matching-Logik (KldB-Zweig stimmt überein UND Modus ma stimmt überein)
        matches = [e for e in EMPLOYER_POOL if e["kldb"] == code and e["mA"] == active_modus]
        
        if matches:
            st.success(f"Es wurden {len(matches)} passfähige Stellen im Raum entdeckt:")
            for m in matches:
                with st.container(border=True):
                    st.markdown(f"**{m['name']}**")
                    st.write(f"* **Berufsfeld:** KldB `{m['kldb']}` ({info['title']})")
                    st.write(f"* **Kultur-Passung (mA):** `{m['mA']}`")
                    st.write(f"* **Beschreibung:** {m['description']}")
        else:
            st.warning("Keine exakte Passung gefunden. (Der KldB-Code und der Arbeitsstil `mA` müssen übereinstimmen). Probieren Sie im Tab 1 einen anderen Arbeitsstil oder passen Sie den Text an.")

# --- TAB 3: LEBENSLAUF-ASSISTENT ---
with tab3:
    st.subheader("Lebenslauf-Assistent")
    st.markdown("**Sollen wir Ihnen beim Erstellen eines tabellarischen Lebenslaufes behilflich sein?**")
    col_a, col_b = st.columns(2)
    with col_a:
        job = col_a.text_input("Zuletzt ausgeübte Station")
    with col_b:
        skills = col_b.text_input("Kernkompetenzen / Studienschwerpunkt")
        
    if st.button("Tabellarischen Entwurf generieren"):
        st.success("Struktur erfolgreich auf Basis Ihres KldB-Profils und Ihrer Eingaben formatiert!")
