import streamlit as st

# Die 15 Prädikaten-Systeme (T1-T15) mit Stammes-Logik
TAXONOMY = {
    "T1": {"name": "Der kalkulierte Erbe", "stamm": "Ökonomisch", "fokus": "Konservierung von Besitz"},
    "T2": {"name": "Der Markt-Akteur", "stamm": "Ökonomisch", "fokus": "Aggressive Expansion"},
    "T3": {"name": "Der strategische Investor", "stamm": "Ökonomisch", "fokus": "Langzeit-Kalkül"},
    "T4": {"name": "Der materielle Ästhet", "stamm": "Ökonomisch", "fokus": "Repräsentativer Konsum"},
    "T5": {"name": "Der funktionale Konservative", "stamm": "Ökonomisch", "fokus": "Stabilitäts-Sicherung"},
    "T6": {"name": "Der klassische Intellektuelle", "stamm": "Kulturell", "fokus": "Asketische Distanz"},
    "T7": {"name": "Der Avantgardist", "stamm": "Kulturell", "fokus": "Grenzüberschreitung"},
    "T8": {"name": "Der Experte", "stamm": "Kulturell", "fokus": "Wissens-Monopol"},
    "T9": {"name": "Der Bildungs-Bürger", "stamm": "Kulturell", "fokus": "Traditions-Verwaltung"},
    "T10": {"name": "Der reflektierte Autodidakt", "stamm": "Kulturell", "fokus": "Institutionelle Distanz"},
    "T11": {"name": "Der Netzwerker", "stamm": "Sozial", "fokus": "Zirkulation von Kontakten"},
    "T12": {"name": "Der Mimikry-Aufsteiger", "stamm": "Sozial", "fokus": "Habitus-Angleichung"},
    "T13": {"name": "Der Broker", "stamm": "Sozial", "fokus": "Transaktions-Gestik"},
    "T14": {"name": "Der prekäre Improvisierer", "stamm": "Sozial", "fokus": "Situations-Zwang"},
    "T15": {"name": "Der System-Spieler", "stamm": "Sozial", "fokus": "Regel-Manipulation"}
}

st.title("Soziologische Maschine: Demystifizierungs-Apparat")

# 1. Bildeingabe & Inputs
uploaded_file = st.file_uploader("Bild laden...", type=["jpg", "png", "webp"])
hexis = st.text_input("Hexis (Beobachtete Haltung):")
doxa = st.text_input("Doxa (Beobachteter Kontext):")
wahl = st.selectbox("Einordnung:", [f"{k}: {v['name']}" for k, v in TAXONOMY.items()])

if st.button("Analysieren"):
    if uploaded_file: st.image(uploaded_file, use_container_width=True)
    
    typ_id = wahl.split(":")[0]
    typ_daten = TAXONOMY[typ_id]
    
    st.subheader("Analyse-Ergebnis")
    
    # 2. Grid-Visualisierung (Schwarz/Grau-Logik)
    cols = st.columns(5)
    for i, (k, v) in enumerate(TAXONOMY.items()):
        with cols[i % 5]:
            if k == typ_id:
                st.markdown(f"**<span style='color:black'>{k}: {v['name']}</span>**", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:grey'>{k}: {v['name']}</span>", unsafe_allow_html=True)
    
    # 3. Kontrastive Begründung
    st.write("---")
    st.write(f"### Analyse-Begründung für {typ_id}: {typ_daten['name']}")
    st.write(f"**Habitus-Indikator:** '{hexis}' im Kontext '{doxa}'.")
    st.write(f"**Stammes-Logik ({typ_daten['stamm']}):** Dieser Typus zeichnet sich primär durch '{typ_daten['fokus']}' aus.")
    
    # Abgrenzung zu anderen Typen des gleichen Stammes
    andere_im_stamm = [f"{k}: {v['fokus']}" for k, v in TAXONOMY.items() if v['stamm'] == typ_daten['stamm'] and k != typ_id]
    st.write(f"**Abgrenzung:** {typ_id} unterscheidet sich von den anderen Typen des {typ_daten['stamm']}-Stammes, da diese auf anderen Schwerpunkten basieren: {', '.join(andere_im_stamm)}.")
    
