import streamlit as st
import re
import math

st.set_page_config(page_title="Topologischer KldB-Raum", layout="wide")

st.title("🌐 Topologischer KldB-Cluster-Raum")
st.markdown("Ihre kumulierten Eingaben spannen einen multidimensionalen Vektor auf. Das System berechnet in Echtzeit die topologische Gravitation zu den KldB-Hauptclustern.")

# Definierte KldB-Cluster mit Merkmalen und Koordinaten im semantischen Raum
CLUSTER_DATA = [
    {
        "id": "it",
        "cluster": "IT, Software & Geoinformatik",
        "code": "Bereich 2 (24xxx/25xxx)",
        "pos_x": 2.0, "pos_y": 8.0,
        "features": {"it", "software", "daten", "code", "logik", "analyse", "algorithmus", "ki", "geografie", "karte", "programmieren", "system"}
    },
    {
        "id": "kultur",
        "cluster": "Kultur, Medien & Archiv",
        "code": "Bereich 3 (31xxx/34xxx)",
        "pos_x": 8.0, "pos_y": 7.0,
        "features": {"historisch", "geschichte", "archiv", "kultur", "bibliothek", "text", "quellen", "sammlung", "karte", "landkarte", "lesen", "schreiben"}
    },
    {
        "id": "natur",
        "cluster": "Landwirtschaft, Natur & Vermessung",
        "code": "Bereich 7 (71xxx)",
        "pos_x": 3.0, "pos_y": 2.0,
        "features": {"natur", "tier", "tiere", "garten", "pflanzen", "erde", "grün", "wald", "umwelt", "vermessung", "draußen"}
    },
    {
        "id": "sozial",
        "cluster": "Gesundheit, Soziales & Pädagogik",
        "code": "Bereich 8 (81xxx)",
        "pos_x": 8.0, "pos_y": 2.0,
        "features": {"gesundheit", "krank", "pflege", "sozial", "helfen", "menschen", "kinder", "alt", "beratung", "medizin", "lehr"}
    },
    {
        "id": "wirtschaft",
        "cluster": "Wirtschaft, Verwaltung & Recht",
        "code": "Bereich 6 (61xxx)",
        "pos_x": 5.0, "pos_y": 5.0,
        "features": {"verwaltung", "amt", "recht", "wirtschaft", "organisation", "büro", "dokument", "struktur"}
    }
]

# Session State initialisieren
if "history" not in st.session_state:
    st.session_state.history = []
if "input_box" not in st.session_state:
    st.session_state.input_box = ""

def add_input():
    text = st.session_state.input_box.strip()
    if text:
        st.session_state.history.append(text)
        st.session_state.input_box = ""

# --- 1. SEKTION: INPUT ---
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("1. Kumulativer Input")
    st.text_input("Geben Sie Facetten ein:", key="input_box", on_change=add_input, placeholder="z.B. historische Landkarten...")
    
    if st.button("Eingabe hinzufügen", type="primary"):
        add_input()
    
    if st.button("Raum zurücksetzen"):
        st.session_state.history = []
        st.session_state.input_box = ""

    if st.session_state.history:
        st.markdown("**Akkumulierter Vektor (Historie):**")
        for i, h in enumerate(st.session_state.history, 1):
            st.caption(f"[{i}] „{h}“")

# --- 2. SEKTION: TOPOLOGISCHE BERECHNUNG & GRAVITATION ---
with col_right:
    st.subheader("2. Topologischer Gravitations-Standort")
    
    # Korpus auswerten
    full_corpus = " ".join(st.session_state.history).lower()
    user_tokens = set(re.findall(r'\b\w+\b', full_corpus))
    
    # Berechne den dynamischen Vektor (Schwerpunkt im Raum ausgehend von (5, 5))
    u_x, u_y = 5.0, 5.0
    cluster_results = []
    
    for c in CLUSTER_DATA:
        matches = user_tokens.intersection(c["features"])
        score = len(matches)
        
        if score > 0:
            # Gravitationskraft zieht den Standort zum Cluster-Mittelpunkt
            u_x += (c["pos_x"] - 5.0) * (score * 0.35)
            u_y += (c["pos_y"] - 5.0) * (score * 0.35)
            
        cluster_results.append({
            "cluster": c["cluster"],
            "code": c["code"],
            "score": score,
            "matches": list(matches)
        })

    # Koordinaten im Rahmen [0, 10] halten
    u_x = max(0.0, min(10.0, u_x))
    u_y = max(0.0, min(10.0, u_y))

    # Visuelle Koordinaten-Box als Ersatz für Plotly
    with st.container(border=True):
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Topologische X-Koordinate", f"{u_x:.2f}")
        col_m2.metric("Topologische Y-Koordinate", f"{u_y:.2f}")
        col_m3.metric("Akkumulierte Tokens", len(user_tokens))
        
        if not user_tokens:
            st.info("Standort im neutralen Zentrum (5.0, 5.0). Fügen Sie links Text hinzu, um den Punkt zu bewegen.")
        else:
            st.success(f"📍 Ihr aktueller Gravitationspunkt im KldB-Raum wurde errechnet.")

# --- 3. SEKTION: CLUSTER-RESONANZ & NÄHE ---
st.divider()
st.subheader("3. Resonanz in den KldB-Hauptclustern")

# Nach Score sortieren
cluster_results.sort(key=lambda x: x["score"], reverse=True)

cols = st.columns(len(cluster_results))
for idx, res in enumerate(cluster_results):
    with cols[idx]:
        with st.container(border=True):
            st.markdown(f"**{res['cluster']}**")
            st.caption(res["code"])
            st.metric("Resonanz-Score", res["score"])
            if res["matches"]:
                st.write(f"✨ Treffer: `{', '.join(res['matches'])}`")
            else:
                st.caption("Keine direkte Resonanz.")
