import streamlit as st

# Die 15 Archetypen mit ihrer logischen Anforderung (Bedeutungseinschluss)
ARCHETYPEN = {
    "T1": {"name": "Der kalkulierte Erbe", "anforderung": ["P_Besitz", "P_Konservierung"]},
    "T2": {"name": "Der Markt-Akteur", "anforderung": ["P_Besitz", "P_Expansion"]},
    # ... (Ergänzen Sie hier T3-T15 analog)
}

st.title("Soziologische Maschine: Demystifizierungs-Apparat")

uploaded_file = st.file_uploader("Bild laden...")
hexis = st.text_input("Hexis (z.B. konzentriert):")
doxa = st.text_input("Doxa (z.B. Börse):")
# Hier geben wir die Prädikate als Daten-Basis ein, die das Bild belegen
prädikate = st.multiselect("Beweis-Prädikate aus Bild:", ["P_Besitz", "P_Expansion", "P_Konservierung", "P_Bildung", "P_Relation"])

if st.button("Analysieren"):
    # Logik-Kern: Welcher Typ wird durch die Prädikate gestützt?
    match = None
    for k, v in ARCHETYPEN.items():
        if set(v["anforderung"]).issubset(set(prädikate)):
            match = k
            break # Erster valider Treffer (Wessel'sche Konsistenz)

    st.subheader("Analyse-Ergebnis")
    
    # Visualisierung
    cols = st.columns(5)
    for i, (k, v) in enumerate(ARCHETYPEN.items()):
        with cols[i % 5]:
            # Nur wenn der Typ logisch durch die Prädikate gedeckt ist, wird er schwarz
            if match and k == match:
                st.markdown(f"**<span style='color:black'>{k}: {v['name']}</span>**", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:grey'>{k}: {v['name']}</span>", unsafe_allow_html=True)

    if match:
        st.write(f"### Begründung für {match}:")
        st.write(f"Das Bild belegt {prädikate}. Diese erfüllen zwingend den Bedeutungseinschluss von {match}.")
    else:
        st.error("Keine logische Konsistenz. Das Bild enthält nicht genügend Prädikate für einen Archetyp.")
