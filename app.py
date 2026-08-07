import streamlit as st
import plotly.graph_objects as go

# Seitenkonfiguration
st.set_page_config(
    page_title="KldB Logik-Parser & Topologie",
    page_icon="⚖️",
    layout="wide"
)

st.title("Bundesagentur für Arbeit – Logik-Parser & Topologie-Engine")
st.markdown("Deterministisches Matching von Bewerberprofilen im hierarchischen KldB-Raum (Klassifikation der Berufe 2010).")

# Sidebar für Eingaben
st.sidebar.header("1. Eingabeparameter")
applicant_bio = st.sidebar.text_area(
    "Freitext-Profil des Bewerbers",
    "Ich habe eine Ausbildung im Bereich Elektrotechnik abgeschlossen, arbeite praxisorientiert und suche eine feste Anstellung in der Betriebstechnik. Wichtig: Absolut keine Nachtschicht."
)
target_kldb = st.sidebar.text_input("Ziel-KldB-Schlüssel (5-stellig)", "25132")

# Hintergrund-Parser (Simulation der Logik-Extraktion)
def parse_bio_to_logic(text):
    lower = text.lower()
    positive = []
    negative = []
    mode = "Direkteinsatz-Modus"

    if "elektrotechnik" in lower or "elektroniker" in lower:
        positive.append("Qualifikation_Elektrotechnik")
    if "betriebstechnik" in lower:
        positive.append("Ziel_Betriebstechnik")
    if "praxisorientiert" in lower:
        positive.append("Praxisorientierte_Arbeitsweise")
        
    if "keine nachtschicht" in lower or "nachtschicht" in lower:
        if "keine nachtschicht" in lower:
            negative.append("Ausschluss_Schichtarbeit")

    if "quereinstieg" in lower:
        mode = "Entwicklungs- & Qualifizierungs-Vektor"

    return {
        "mA": mode,
        "↓A": positive,
        "↑A": negative
    }

# Berechnung der topologischen Distanz im KldB-Baum
def get_topological_distance(applicant_inferred_code, target_code):
    match_level = 0
    for i in range(min(len(applicant_inferred_code), len(target_code))):
        if applicant_inferred_code[i] == target_code[i]:
            match_level = i + 1
        else:
            break
    # Distanz: 0 bedeutet identisch auf Ebene 5, max 5
    return 5 - match_level, match_level

if st.sidebar.button("Matching & Topologie berechnen", type="primary"):
    # Validierung des Zielschlüssels
    if len(target_kldb) != 5 or not target_kldb.isdigit():
        st.error("Bitte geben Sie einen gültigen 5-stelligen numerischen KldB-Schlüssel ein (z. B. 25132).")
    else:
        # Parsen ausführen
        profile = parse_bio_to_logic(applicant_bio)
        
        # Angenommener passender Basis-Code aus dem Profil für den Distanz-Vergleich (hier simuliert auf Basis der Extraktion)
        applicant_code = "25132" if "elektrotechnik" in applicant_bio.lower() else "43414"
        
        dist, match_lvl = get_topological_distance(applicant_code, target_kldb)

        # Layout in Spalten
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Logische Extraktion (Parser)")
            st.info(f"**Modus (mA):** {profile['mA']}")
            
            # Korrigierte Ausgabe für Positiv-Bedingungen
            pos_text = ", ".join(profile['↓A']) if profile['↓A'] else "Keine"
            st.success(f"**Tatsachen / Positiv (↓A):** {pos_text}")
            
            if profile['↑A']:
                st.error(f"**Dealbreaker / Ausschluss (↑A):** {', '.join(profile['↑A'])}")
            else:
                st.write("**Dealbreaker (↑A):** Keine harten Ausschlüsse erkannt.")

        with col2:
            st.subheader("Topologischer Baum-Abgleich")
            st.metric("Übereinstimmende KldB-Ebene", f"Ebene {match_lvl} von 5")
            st.metric("Topologische Distanz (Baum-Metrik)", f"{dist} Schritte")
            
            # Kollisionsprüfung
            collision = "Ausschluss_Schichtarbeit" in profile['↑A'] and target_kldb == "25132"
            if collision:
                st.warning("⚠️ **Kollisions-Check:** Match-Verhinderung wegen Schichtdienst-Ausschluss!")
            else:
                st.success("✅ **Kollisions-Check:** Keine harten Konflikte festgestellt.")

        st.markdown("---")
        st.subheader("Visualisierung der topologischen Nähe (Hierarchie-Ebenen)")

        # Erstellung der Visualisierung mit Plotly (Baum-Tiefe)
        levels = [
            "1. Berufsabschnitt", 
            "2. Berufsbereich", 
            "3. Berufsgruppe", 
            "4. Berufsfamilie", 
            "5. Einzelberuf & Niveau"
        ]
        
        # Ermitteln, welche Ebenen übereinstimmen
        match_flags = [1 if i < match_lvl else 0 for i in range(5)]
        colors = ['#003366' if flag == 1 else '#cbd5e1' for flag in match_flags]
        sub_codes = [target_kldb[:i+1] for i in range(5)]

        fig = go.Figure(data=[
            go.Bar(
                x=levels,
                y=[1, 1, 1, 1, 1],
                marker_color=colors,
                text=[f"Code: {c}" for c in sub_codes],
                textposition='auto',
                hoverinfo='text'
            )
        ])

        fig.update_layout(
            title=f"Hierarchischer Pfad im KldB-Raum für Zielschlüssel {target_kldb}",
            yaxis=dict(showticklabels=False, range=[0, 1.4]),
            xaxis=dict(title="Hierarchie-Ebene der Klassifikation"),
            template="plotly_white",
            margin=dict(t=40, b=20, l=20, r=20)
        )

        st.plotly_chart(fig, use_container_width=True)
