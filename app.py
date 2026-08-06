import streamlit as st

# --- Konfiguration & Datenbank ---
KLDB_DATABASE = {
    "24104": {"title": "Softwareentwicklung & KI", "beschreibung": "Entwicklung komplexer Systeme"},
    "71102": {"title": "Garten- & Landschaftsbau", "beschreibung": "Gestaltung von Naturräumen"},
    "81403": {"title": "Soziale Arbeit", "beschreibung": "Beratung & Pädagogik"},
    "25192": {"title": "Wissenschaft & Forschung", "beschreibung": "Theorie & Konzeptentwicklung"}
}

# Einfache Arbeitgeber-Datenbank
EMPLOYER_POOL = [
    {"name": "KI-Forschungsinstitut", "kldb": "24104", "mA": "Autonom & Eigenverantwortlich", "kA": "KI & Technologie"},
    {"name": "Digital-StartUp", "kldb": "24104", "mA": "Agil & Interdisziplinär", "kA": "KI & Technologie"},
    {"name": "Stadtgarten GmbH", "kldb": "71102", "mA": "Strukturiert & Klassisch", "kA": "Natur & Umwelt"}
]

st.set_page_config(page_title="Arbeitsmarkt-Lotse", layout="centered")

# --- UI Styling ---
st.title("🤝 Arbeitsmarkt-Lotse")
st.markdown("Finden wir gemeinsam den Platz, der wirklich zu Ihnen passt.")

# --- Tabs für die intuitive Führung ---
tab1, tab2, tab3 = st.tabs(["1. Über mich", "2. Passende Stellen", "3. Lebenslauf-Hilfe"])

# --- TAB 1: EINGABE ---
with tab1:
    st.subheader("Erzählen Sie uns von Ihrer Vision")
    story = st.text_area("Was motiviert Sie? Wie arbeiten Sie am liebsten? Schreiben Sie einfach frei darauf los...", 
                         height=150, 
                         placeholder="Beispiel: Ich liebe logische Strukturen, arbeite gerne eigenständig und interessiere mich für KI...")
    
    col1, col2 = st.columns(2)
    modus = col1.radio("Mein Arbeitsstil", ["Autonom & Eigenverantwortlich", "Agil & Interdisziplinär", "Strukturiert & Klassisch"])
    kontext = col2.radio("Mein Umfeld", ["KI & Technologie", "Öffentlicher Sektor", "Wissenschaft & Bildung", "Natur & Umwelt"])

    if st.button("Profil analysieren", type="primary"):
        st.session_state["story"] = story
        st.session_state["modus"] = modus
        st.session_state["kontext"] = kontext
        st.success("Profil gespeichert! Gehen Sie zu 'Passende Stellen'.")

# --- TAB 2: MATCHING ---
with tab2:
    st.subheader("Ihre optimalen Match-Partner")
    
    if "story" not in st.session_state:
        st.info("Bitte füllen Sie zuerst unter '1. Über mich' Ihr Profil aus.")
    else:
        # Mini-Logik zur KldB-Zuordnung (simuliert)
        detected_kldb = "24104" if "logik" in st.session_state["story"].lower() or "ki" in st.session_state["story"].lower() else "71102"
        
        # Matching-Filter
        matches = [e for e in EMPLOYER_POOL if e["kldb"] == detected_kldb and e["mA"] == st.session_state["modus"]]
        
        st.markdown(f"**Analyse:** Basierend auf Ihrem Text passen Sie zum Bereich *{KLDB_DATABASE[detected_kldb]['title']}*.")
        
        if matches:
            for m in matches:
                with st.container(border=True):
                    st.write(f"### {m['name']}")
                    st.caption(f"Passung: Bereich {m['kldb']} | Stil: {m['mA']}")
                    st.button("Details anzeigen", key=m['name'])
        else:
            st.warning("Keine exakten Matches gefunden. Probieren Sie eine andere Kombination aus Arbeitsstil oder Kontext!")

# --- TAB 3: LEBENSLAUF ---
with tab3:
    st.subheader("Lebenslauf-Assistent")
    st.write("Wir helfen Ihnen, Ihre Erfahrungen in eine tabellarische Form zu bringen.")
    
    col_a, col_b = st.columns(2)
    job = col_a.text_input("Zuletzt gearbeitet als")
    skills = col_b.text_input("Kernkompetenz")
    
    if st.button("Entwurf erstellen"):
        st.write("---")
        st.write(f"**Vorläufige Struktur für: {job}**")
        st.write(f"- Fokus: {skills}")
        st.write("- [Hier würde ein professioneller Lebenslauf-Entwurf generiert werden]")
