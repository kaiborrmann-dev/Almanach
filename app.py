import streamlit as st
import plotly.express as px
import pandas as pd
import re

st.set_page_config(page_title="Topologischer KldB-Cluster-Raum", layout="wide")

st.title("🌐 KldB-Raum als topologische Cluster-Landschaft")
st.markdown("Ihre kumulierten Eingaben bestimmen Ihre Koordinaten im Raum. Der Graph zeigt in Echtzeit, welchem KldB-Cluster Sie sich topologisch annähern.")

# Definierte KldB-Cluster mit festen 2D-Koordinaten im semantischen Raum und Merkmalen
CLUSTER_DATA = [
    {
        "cluster": "IT, Software & Geoinformatik",
        "code": "Bereich 2 (24xxx/25xxx)",
        "x": 2.0, "y": 8.0,
        "features": {"it", "software", "daten", "code", "logik", "analyse", "algorithmus", "ki", "geografie", "karte", "programmieren"}
    },
    {
        "cluster": "Kultur, Medien & Archiv",
        "code": "Bereich 3 (31xxx/34xxx)",
        "x": 8.0, "y": 7.0,
        "features": {"historisch", "geschichte", "archiv", "kultur", "bibliothek", "text", "quellen", "sammlung", "karte", "landkarte"}
    },
    {
        "cluster": "Landwirtschaft, Natur & Vermessung",
        "code": "Bereich 7 (71xxx)",
        "x": 3.0, "y": 2.0,
        "features": {"natur", "tier", "tiere", "garten", "pflanzen", "erde", "grün", "wald", "umwelt", "vermessung"}
    },
    {
        "cluster": "Gesundheit, Soziales & Pädagogik",
        "code": "Bereich 8 (81xxx)",
        "x": 8.0, "y": 2.0,
        "features": {"gesundheit", "krank", "pflege", "sozial", "helfen", "menschen", "kinder", "alt", "beratung", "medizin"}
    },
    {
        "cluster": "Wirtschaft, Verwaltung & Recht",
        "code": "Bereich 6 (61xxx)",
        "x": 5.0, "y": 5.0,
        "features": {"verwaltung", "amt", "recht", "wirtschaft", "organisation", "büro", "dokument"}
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

# --- 1. EINGABE-BEREICH ---
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
        st.markdown("**Akkumulierter Vektor:**")
        for i, h in enumerate(st.session_state.history, 1):
            st.caption(f"[{i}] „{h}“")

# --- 2. BERECHNUNG DER KOORDINATEN & PLOTLY CLUSTER MAP ---
with col_right:
    st.subheader("2. Topologischer Cluster-Raum")
    
    # Gesamten Korpus auswerten
    full_corpus = " ".join(st.session_state.history).lower()
    user_tokens = set(re.findall(r'\b\w+\b', full_corpus))
    
    # Dynamische Berechnung des Nutzer-Schwerpunkts (Gravitationszentrum)
    # Startpunkt ist die Mitte (5.0, 5.0)
    u_x, u_y = 5.0, 5.0
    total_weight = 1.0
    
    cluster_scores = []
    for c in CLUSTER_DATA:
        matches = user_tokens.intersection(c["features"])
        score = len(matches)
        cluster_scores.append({"cluster": c["cluster"], "score": score})
        
        if score > 0:
            # Gravitations-Verschiebung in Richtung des Clusters
            u_x += (c["x"] - 5.0) * (score * 0.4)
            u_y += (c["y"] - 5.0) * (score * 0.4)
            total_weight += score

    # DataFrame für Plotly aufbauen
    df_clusters = pd.DataFrame(CLUSTER_DATA)
    df_clusters["Typ"] = "KldB-Cluster"
    df_clusters["Größe"] = 25
    
    # Nutzer-Punkt hinzufügen
    df_user = pd.DataFrame([{
        "cluster": "📍 Ihr Standort (Aktuelles Profil)",
        "code": "Dynamischer Vektor",
        "x": u_x,
        "y": u_y,
        "Typ": "Ihr Profil",
        "Größe": 40
    }])
    
    df_plot = pd.concat([df_clusters, df_user], ignore_index=True)
    
    # Scatter-Plot erstellen
    fig = px.scatter(
        df_plot, 
        x="x", 
        y="y", 
        color="Typ", 
        size="Größe",
        text="cluster",
        hover_data=["code"],
        color_discrete_map={"KldB-Cluster": "#1f77b4", "Ihr Profil": "#ff7f0e"}
    )
    
    fig.update_traces(textposition='top center')
    fig.update_layout(
        xaxis=dict(range=[0, 10], showgrid=True, zeroline=False),
        yaxis=dict(range=[0, 10], showgrid=True, zeroline=False),
        height=450,
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# --- 3. DETAIL-ANALYSE DER NÄHE ---
st.divider()
st.subheader("3. Cluster-Resonanz & topologische Distanz")

if not user_tokens:
    st.info("Der Raum befindet sich im neutralen Zentrum (5,5). Fügen Sie Aussagen hinzu, um die Gravitation zu aktivieren.")
else:
    # Sortiere nach Treffern
    cluster_scores.sort(key=lambda x: x["score"], reverse=True)
    
    cols = st.columns(len(cluster_scores))
    for idx, cs in enumerate(cluster_scores):
        with cols[idx]:
            st.metric(label=cs["cluster"], value=f"Treffer: {cs['score']}")
