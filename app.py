import streamlit as st

# Die 15 Prädikaten-Systeme (T1-T15)
TAXONOMY = {
    "T1": {"name": "Der kalkulierte Erbe", "stamm": "Ökonomisch"},
    "T2": {"name": "Der Markt-Akteur", "stamm": "Ökonomisch"},
    "T3": {"name": "Der strategische Investor", "stamm": "Ökonomisch"},
    "T4": {"name": "Der materielle Ästhet", "stamm": "Ökonomisch"},
    "T5": {"name": "Der funktionale Konservative", "stamm": "Ökonomisch"},
    "T6": {"name": "Der klassische Intellektuelle", "stamm": "Kulturell"},
    "T7": {"name": "Der Avantgardist", "stamm": "Kulturell"},
    "T8": {"name": "Der Experte", "stamm": "Kulturell"},
    "T9": {"name": "Der Bildungs-Bürger", "stamm": "Kulturell"},
    "T10": {"name": "Der reflektierte Autodidakt", "stamm": "Kulturell"},
    "T11": {"name": "Der Netzwerker", "stamm": "Sozial"},
    "T12": {"name": "Der Mimikry-Aufsteiger", "stamm": "Sozial"},
    "T13": {"name": "Der Broker", "stamm": "Sozial"},
    "T14": {"name": "Der prekäre Improvisierer", "stamm": "Sozial"},
    "T15": {"name": "Der System-Spieler", "stamm": "Sozial"}
}

st.title("Soziologische Maschine")

# 1. Bildeingabe
uploaded_file = st.file_uploader("Bild eingeben...", type=["jpg", "png", "webp"])

# 2. Input-Felder
hexis = st.text_input("Hexis (Beobachtete Haltung):")
doxa = st.text_input("Doxa (Beobachteter Kontext):")
wahl = st.selectbox("Einordnung (Wähle den passenden Typ):", [f"{k}: {v['name']}" for k, v in TAXONOMY.items()])

if st.button("Analysieren"):
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)
    
    typ_id = wahl.split(":")[0]
    
    st.subheader("Analyse-Ergebnis")
    
    # Grid der 15 Typen
    cols = st.columns(5)
    for i, (k, v) in enumerate(TAXONOMY.items()):
        with cols[i % 5]:
            if k == typ_id:
                st.markdown(f"**{k}: {v['name']}**") # Schwarz/Fett
            else:
                st.markdown(f"<span style='color:grey'>{k}: {v['name']}</span>", unsafe_allow_html=True)
    
    st.write("---")
    st.write(f"**Begründung für {typ_id}:**")
    st.write(f"Das Subjekt zeigt eine {hexis}-Haltung im {doxa}-Kontext. Dies korrespondiert mit der Kapitalstruktur '{TAXONOMY[typ_id]['stamm']}' des Typus {typ_id}.")
