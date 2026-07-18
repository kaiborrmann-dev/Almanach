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
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    client = OpenAI()

ATLAS_FILE = "habitus_atlas_100.json"

# --- ECHTE FALLBACK-DATEN (Falls die API fehlschlägt oder das JSON verzerrt ist) ---
FALLBACK_DATABASE = [
    {"id": 1, "name": "Amal & George Clooney", "cat": "Global Elite / Intellektuell"},
    {"id": 2, "name": "Victoria & David Beckham", "cat": "Power-Duo / Lifestyle-Brand"},
    {"id": 3, "name": "Beyoncé & Jay-Z", "cat": "Kulturelle Hegemonie / Industrie"},
    {"id": 4, "name": "Michelle & Barack Obama", "cat": "Moralisch-Institutionelle Elite"},
    {"id": 5, "name": "Zendaya & Tom Holland", "cat": "Next-Gen Pop / Nahbar"},
    {"id": 6, "name": "Prinz Harry & Meghan Markle", "cat": "Disrupte Aristokratie / Expressiv"},
    {"id": 7, "name": "Greta Gerwig & Noah Baumbach", "cat": "Intellektuelles Kino / Arthouse"},
    {"id": 8, "name": "Lauren Sánchez & Jeff Bezos", "cat": "Jetset-Kapitalismus / Performance"},
    {"id": 9, "name": "Priscilla Chan & Mark Zuckerberg", "cat": "Rationelle Tech-Philanthropie"},
    {"id": 10, "name": "Taylor Swift & Travis Kelce", "cat": "Hyper-Mainstream Hegemonie"},
    {"id": 11, "name": "Robert Habeck & Andrea Paluch", "cat": "Bürgerlich-Pragmatischer Diskurs"},
    {"id": 12, "name": "Rihanna & A$AP Rocky", "cat": "Avantgarde Pop / Street Culture"},
    {"id": 13, "name": "Eva Mendes & Ryan Gosling", "cat": "Diskrete Hollywood-Symmetrie"},
    {"id": 14, "name": "Penélope Cruz & Javier Bardem", "cat": "Expressives Charakter-Kino"}
]

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

    Für jedes Paar musst du die öffentliche Wahrnehmung auf einer Skala von 1 bis 10 für die folgenden vier Achsen bewerten:
    {AXES_DEFINITION}

    Gib das Ergebnis AUSSCHLIESSLICH als valides JSON-Array aus. Keine Erklärung, kein Markdown außerhalb des JSON-Blocks.

    JSON-Format:
    [
      {{
        "id": 1,
        "name": "Name 1 & Name 2",
        "cat": "Kategorie-Typus",
        "v": [5, 9, 8, 10]
      }}
    ]
    """
    
    with st.spinner("🤖 Generiere 100 lebende Paare via OpenAI..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": "Generiere genau 100 lebende Paare als JSON-Liste."}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            if content.startswith("```json"):
                content = content.split("```json")[1].split("```")[0].strip()
            elif content.startswith("```"):
                content = content.split("```")[1].split("```")[0].strip()
            
            raw_data = json.loads(content)
            
            # Unter-Keys auflösen falls vorhanden
            if isinstance(raw_data, dict):
                for key, val in raw_data.items():
                    if isinstance(val, list):
                        raw_data = val
                        break
            
            if not isinstance(raw_data, list) and isinstance(raw_data, dict):
                raw_data = list(raw_data.values())

            clean_data = []
            for index, item in enumerate(raw_data):
                if isinstance(item, dict) and ("name" in item or "paar" in item):
                    clean_data.append({
                        "id": int(item.get("id", index + 1)),
                        "name": item.get("name", item.get("paar", "Unbekannt")),
                        "cat": item.get("cat", item.get("kategorie", "Allgemein")),
                        "v": item.get("v", item.get("vektor", [5, 5, 5, 5]))
                    })
            
            if len(clean_data) > 0:
                with open(ATLAS_FILE, "w", encoding="utf-8") as f:
                    json.dump(clean_data, f, indent=2, ensure_ascii=False)
                return clean_data
        except Exception as api_err:
            st.sidebar.warning(f"API Details übersprungen: {api_err}")
            
    return FALLBACK_DATABASE

# --- DATEN BEZIEHEN ---
if os.path.exists(ATLAS_FILE):
    try:
        with open(ATLAS_FILE, "r", encoding="utf-8") as f:
            PAAR_DATABASE = json.load(f)
        if not PAAR_DATABASE or len(PAAR_DATABASE) == 0:
            PAAR_DATABASE = FALLBACK_DATABASE
    except Exception:
        PAAR_DATABASE = FALLBACK_DATABASE
else:
    PAAR_DATABASE = generate_zeitgeist_atlas()

# --- REALE TOPOLOGISCHE USER-DATENBANK ---
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
    
    if st.button("🔄 Atlas via OpenAI neu eichen"):
        if os.path.exists(ATLAS_FILE):
            os.remove(ATLAS_FILE)
        st.rerun()

    # Optionen erstellen
    paar_options = {}
    for p in PAAR_DATABASE:
        paar_options[p["id"]] = f"{p['name']} ({p['cat']})"

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
