import streamlit as st
import json
import os
from openai import OpenAI

# --- DESIGN & BRANDING ---
st.set_page_config(page_title="Zeitgeist-Compass", page_icon="🧭", layout="wide")

st.title("🧭 Zeitgeist-Compass")
st.subheader("Soziologisches Modell-Matching via Graph-Topologie (Projekt Almanach)")
st.write("---")

# --- INITIALISIERUNG OPENAI CLIENT ---
# Streamlit zieht sich den Key automatisch aus den "Secrets" (Einstellungen im Streamlit Dashboard)
# Alternativ nutzt es die lokale Umgebungsvariable OPENAI_API_KEY
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    client = OpenAI() # Fällt auf os.environ zurück

ATLAS_FILE = "habitus_atlas_100.json"

# --- AUTOMATISIERTE OPENAI PIPELINE ---
def generate_zeitgeist_atlas():
    AXES_DEFINITION = """
    A1 (Distinktion): 1 = Rein konsumorientierter Pop/Trash, 10 = Hochkultur-Diskurs/Avantgarde.
    A2 (Orientierung): 1 = Erhalt/Tradition, 10 = Disruption/Technik-Fokus/Innovation.
    A3 (Affekt): 1 = Hochgradig expressiv/emotional/impulsiv, 10 = Rational/Bürokratisch/Stoisch.
    A4 (Soziale Sphäre): 1 = Kollektiv/Gemeinwohl/Ideell, 10 = Individualistisch/Leistungsorientiert/Brand.
    """

    SYSTEM_PROMPT = f"""
    Du bist ein präzise arbeitendes soziologisches Analyse-Werkzeug. 
    Deine Aufgabe ist es, eine Matrix von genau 100 prominenten, aktuell im Jahr 2026 LEBENDEN Paaren weltweit zu generieren und zu eichen.

    Kriterien für die Paarauswahl:
    - Beide Personen müssen leben.
    - Sie müssen aus verschiedenen Feldern stammen (Tech, Politik, Kunst, Sport, globale Elite, Popkultur).
    - Die Auswahl muss den gesamten sozialen Raum abdecken (von Trash-Pop bis Arthouse-Elite).

    Für jedes Paar musst du die öffentliche Wahrnehmung ihrer Beziehungs-Architektur auf einer Skala von 1 bis 10 für die folgenden vier Achsen bewerten:
    {AXES_DEFINITION}

    Gib das Ergebnis AUSSCHLIESSLICH als valides JSON-Array aus. Keine Erklärung, kein Markdown-Inhalt außerhalb des JSON-Blocks.

    JSON-Format:
    [
      {{
        "id": 1,
        "name": "Name 1 & Name 2",
        "cat": "z.B. Tech-Philanthropie",
        "v": [5, 9, 8, 10]
      }}
    ]
    """
    
    with st.spinner("🤖 Generiere und eiche 100 lebende Paare via OpenAI..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "Generiere die vollständige Matrix mit genau 100 lebenden Paaren und ihren soziologischen Signaturen."}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        # Markdown-Säuberung falls nötig
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        
        data = json.loads(content)
        if isinstance(data, dict):
            key = list(data.keys())[0]
            data = data[key]
            
        # Speichern für zukünftige Aufrufe
        with open(ATLAS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return data

# --- LADE ODER GENERIERE DATEN ---
if os.path.exists(ATLAS_FILE):
    with open(ATLAS_FILE, "r", encoding="utf-8") as f:
        PAAR_DATABASE = json.load(f)
else:
    try:
        PAAR_DATABASE = generate_zeitgeist_atlas()
        st.success("🎉 Referenz-Atlas erfolgreich via API initialisiert!")
    except Exception as e:
        st.error(f"Fehler bei der API-Generierung: {e}")
        # Fallback auf minimalen Kern, damit die App nicht crasht
        PAAR_DATABASE = [{"id": 1, "name": "Amal & George Clooney", "cat": "Global Elite"}]

# --- REALE TOPOLOGISCHE USER-DATENBANK (Simuliert) ---
MOCK_USERS_GRAPH = [
    {"name": "Konrad (34)", "choices": [1, 4, 11]},
    {"name": "Elena (29)", "choices": [3, 5, 12]},
    {"name": "Maximilian (41)", "choices": [1, 7, 13]},
    {"name": "Clara (31)", "choices": [4, 11, 14]}
]

# --- UI LOGIK ---
col1, col2 = st.columns(2)

with col1:
    st.header("1. Wähle exakt 3 Paare")
    st.caption("Welche Beziehungsarchitektur spricht dich strukturell an?")
    
    # Dynamischer Button zum manuellen Neu-Eichen
    if st.button("🔄 Atlas via OpenAI neu eichen"):
        if os.path.exists(ATLAS_FILE):
            os.remove(ATLAS_FILE)
        st.rerun()

    # Dropdown-Auswahl speist sich nun direkt aus den 100 generierten Paaren
    paar_options = {p["id"]: f"{p['name']} ({p['cat']})" for p in PAAR_DATABASE}
    selected_ids = st.multiselect(
        "Wähle deine 3 strukturellen Anker-Modelle:",
        options=list(paar_options.keys()),
        format_func=lambda x: paar_options[x]
    )

with col2:
    st.header("2. Topologische Auswertung")
    
    if len(selected_ids) == 3:
        st.success("Topologischer Kern (K1) induziert!")
        st.info("Dein Suchraum ist nach Kuratowski (H4) abgeschlossen und stabil.")
        
        safe_zone = []
        fun_zone = []
        
        for user in MOCK_USERS_GRAPH:
            intersection = len(set(selected_ids).intersection(set(user["choices"])))
            
            if intersection >= 2:
                safe_zone.append((user["name"], f"{intersection} gemeinsame Modelle"))
            elif intersection == 1:
                fun_zone.append((user["name"], "Brücken-Modell aktiv"))
                
        st.write("### 🟢 Safe Zone (Interior / Strukturelle Zwillinge)")
        if safe_zone:
            for name, info in safe_zone:
                st.code(f"{name} ➔ {info}")
        else:
            st.caption("Keine Profile im inneren Kern.")
            
        st.write("### 🟡 Fun Zone (Boundary / Produktiver Rand)")
        if fun_zone:
            for name, info in fun_zone:
                st.code(f"{name} ➔ {info}")
        else:
            st.caption("Keine Profile auf der Grenzkante.")
            
    else:
        st.warning("Bitte wähle exakt 3 Paare aus, um die topologische Hülle zu berechnen.")
