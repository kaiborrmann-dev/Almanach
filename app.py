import streamlit as st

# Die 15 Archetypen-Datenbank
ARCHETYPEN = {
    "T1": {"name": "Der kalkulierte Erbe", "kapital": "Ökonomisch"},
    "T2": {"name": "Der Markt-Akteur", "kapital": "Ökonomisch"},
    "T3": {"name": "Der strategische Investor", "kapital": "Ökonomisch"},
    "T4": {"name": "Der materielle Ästhet", "kapital": "Ökonomisch"},
    "T5": {"name": "Der funktionale Konservative", "kapital": "Ökonomisch"},
    "T6": {"name": "Der klassische Intellektuelle", "kapital": "Kulturell"},
    "T7": {"name": "Der Avantgardist", "kapital": "Kulturell"},
    "T8": {"name": "Der Experte", "kapital": "Kulturell"},
    "T9": {"name": "Der Bildungs-Bürger", "kapital": "Kulturell"},
    "T10": {"name": "Der reflektierte Autodidakt", "kapital": "Kulturell"},
    "T11": {"name": "Der Netzwerker", "kapital": "Sozial"},
    "T12": {"name": "Der Mimikry-Aufsteiger", "kapital": "Sozial"},
    "T13": {"name": "Der Broker", "kapital": "Sozial"},
    "T14": {"name": "Der prekäre Improvisierer", "kapital": "Sozial"},
    "T15": {"name": "Der System-Spieler", "kapital": "Sozial"}
}

st.title("Soziologische Maschine")

# 1. Bildeingabe
uploaded_file = st.file_uploader("Bild eingeben...", type=["jpg", "png", "webp"])

# 2. Input-Felder
hexis = st.text_input("Hexis (Beobachtete Haltung):")
doxa = st.text_input("Doxa (Beobachteter Kontext):")
wahl = st.selectbox("Einordnung (Wähle den passenden Typ):", [f"{k}: {v['name']}" for k, v in ARCHETYPEN.items()])

if st.button("Analysieren"):
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)
    
    typ_id = wahl.split(":")[0]
    
    st.subheader("Analyse-Ergebnis")
    
    # Grid der 15 Typen
    cols = st.columns(5)
    for i, (k, v) in enumerate(ARCHETYPEN.items()):
        with cols[i % 5]:
            if k == typ_id:
                st.markdown(f"**{k}: {v['name']}**") # Schwarz/Fett
            else:
                st.markdown(f"<span style='color:grey'>{k}: {v['name']}</span>", unsafe_allow_html=True)
    
    st.write("---")
    st.write(f"**Begründung für {typ_id}:**")
    st.write(f"Das Subjekt zeigt eine {hexis}-Haltung im {doxa}-Kontext. Dies korrespondiert mit der Kapitalstruktur '{ARCHETYPEN[typ_id]['kapital']}' des Typus {typ_id}.")
