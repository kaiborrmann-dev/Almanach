import streamlit as st
import re

st.set_page_config(page_title="Topologischer Berufs-Raum (KldB)", layout="wide")

st.title("🌐 Topologischer Arbeitsmarkt-Raum")
st.markdown("Die KldB als topologischer Raum: Ihre Eingaben spannen ein Koordinatensystem auf, in dem die **topologische Nähe** der Berufsfelder in Echtzeit berechnet wird.")

# Definition des topologischen Raumes (KldB-Hauptfelder mit ihren semantischen Koordinaten / Merkmalen)
TOPOLOGICAL_SPACE = {
    "2 - IT, Software & Geoinformatik": {
        "code": "24xxx / 25xxx",
        "features": {"ki", "software", "daten", "code", "logik", "analyse", "algorithmus", "struktur", "rechner", "karte", "geografie", "programmieren", "system"},
        "beschreibung": "Formale Systeme, Berechnungen und digitale Architekturen."
    },
    "3 - Geisteswissenschaften, Kultur & Archiv": {
        "code": "31xxx / 34xxx",
        "features": {"historisch", "geschichte", "archiv", "kultur", "bibliothek", "text", "lesen", "schreiben", "quellen", "sammlung", "philosophie", "kunst"},
        "beschreibung": "Kulturelle Überlieferung, Textanalyse und konzeptionelle Deutung."
    },
    "5 - Tourismus, Medien & Gestaltung": {
        "code": "52xxx / 26xxx",
        "features": {"reisen", "foto", "fotografie", "medien", "design", "turismus", "hotel", "welt", "kunden", "kommunikation", "bild", "veranstaltung"},
        "beschreibung": "Mediale Vermittlung, visuelle Gestaltung und Raumwechsel."
    },
    "7 - Landwirtschaft, Natur & Umwelt": {
        "code": "71xxx / 81xxx",
        "features": {"natur", "tier", "tiere", "garten", "pflanzen", "erde", "grün", "wald", "umwelt", "ökologie", "draußen", "hof"},
        "beschreibung": "Arbeit mit lebenden Systemen und natürlichen Räumen."
    },
    "8 - Gesundheit, Soziales & Pädagogik": {
        "code": "81xxx / 83xxx",
        "features": {"gesundheit", "krank", "pflege", "sozial", "helfen", "menschen", "kinder", "alt", "beratung", "unterstützung", "medizin", "lehre"},
        "beschreibung": "Direkte Sorge, Begleitung und soziale Interaktion."
    }
}

# Session State initialisieren
if "user_statements" not in st.session_state:
    st.session_state.user_statements = []
if "current_input" not in st.session_state:
    st.session_state.current_input = ""

def add_statement():
    val = st.session_state.current_input.strip()
    if val:
        st.session_state.user_statements.append(val)
        st.session_state.current_input = ""

# --- 1. EINGABE-BEREICH (Der Phasenraum des Bewerbers) ---
st.subheader("1. Äußerungen & Facetten des Bewerbers")
st.markdown("Geben Sie nacheinander Dinge ein, die Ihnen einfallen – egal ob Vorlieben, Hobbys, Arbeitsweisen oder Fachthemen:")

col_in, col_btn1, col_btn2 = st.columns([3, 1, 1])
with col_in:
    st.text_input("Ihre Äußerung:", key="current_input", on_change=add_statement, placeholder="z.B. Ich sammle historische Landkarten und arbeite gerne logisch...")
with col_btn1:
    st.write("")
    st.button("Hinzufügen", type="primary", on_click=add_statement)
with col_btn2:
    st.write("")
    if st.button("Raum zurücksetzen"):
        st.session_state.user_statements = []
        st.session_state.current_input = ""

# Historie anzeigen
if st.session_state.user_statements:
    st.markdown("**Bisheriges semantisches Profil (Punkt im Raum):**")
    for idx, stmt in enumerate(st.session_state.user_statements, 1):
        st.caption(f"[{idx}] „{stmt}“")

st.divider()

# --- 2. TOPOLOGISCHE NÄHERUNGS-BERECHNUNG ---
st.subheader("2. Topologischer Distanz- und Nähe-Graph der KldB-Felder")

# Gesamten Textkorpus tokenisieren
corpus = " ".join(st.session_state.user_statements).lower()
user_tokens = set(re.findall(r'\b\w+\b', corpus))

# Berechne die Nähe (Jaccard-Ähnlichkeit / Schnittmenge als topologisches Maß)
distances = []
for field_name, data in TOPOLOGICAL_SPACE.items():
    features = data["features"]
    intersection = user_tokens.intersection(features)
    union = user_tokens.union(features)
    
    # Metrik: Schnittmenge im Verhältnis zur Merkmalsmenge des Feldes (Topologische Überlappung)
    if len(features) > 0:
        proximity_score = len(intersection) / len(features)
    else:
        proximity_score = 0.0
        
    # Absoluter Treffer-Count für die Gewichtung
    hit_count = len(intersection)
    
    distances.append({
        "field": field_name,
        "code": data["code"],
        "desc": data["beschreibung"],
        "score": proximity_score,
        "hits": hit_count,
        "matched_features": list(intersection)
    })

# Nach Nähe (Score) sortieren – das ist die topologische Sortierung im Raum!
distances.sort(key=lambda x: (x["score"], x["hits"]), reverse=True)

# Visualisierung des Raums
if not user_tokens:
    st.info("Der topologische Raum ist neutral. Fügen Sie oben Aussagen hinzu, um die Gravitation und Nähe zu den Berufsfeldern zu berechnen.")
else:
    st.markdown("Die Berufsfelder sind nach ihrer **topologischen Nähe** zu Ihren Aussagen sortiert (vom Zentrum des Raumes an die Peripherie):")
    
    for rank, d in enumerate(distances, 1):
        # Visuelle Hervorhebung basierend auf der Nähe
        if d["score"] > 0.15 or d["hits"] > 0:
            border_color = "🟢"
            box_type = "erfolgreich"
        else:
            border_color = "⚪"
            
        with st.container(border=True):
            cols = st.columns([4, 1])
            with cols[0]:
                st.markdown(f"### {border_color} Rang {rank}: {d['field']}")
                st.caption(f"Amtlicher KldB-Bereich: `{d['code']}` | {d['desc']}")
                if d["matched_features"]:
                    st.write(f"✨ **Topologische Schnittpunkte (Resonanzen):** `{', '.join(d['matched_features'])}`")
                else:
                    st.caption("Keine direkte semantische Überschneidung in diesem Bereich (Distanz ist groß).")
            with cols[1]:
                st.metric("Nähe-Score", f"{d['score']:.2f}")
