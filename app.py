import streamlit as st

# Die 15 Prädikaten-Systeme (T1-T15)
TAXONOMY = {
    "T1": {"name": "Der kalkulierte Erbe", "stamm": "Ökonomisch", "abgrenzung": "Konservierung statt Expansion"},
    "T2": {"name": "Der Markt-Akteur", "stamm": "Ökonomisch", "abgrenzung": "Expansion statt Konservierung"},
    "T3": {"name": "Der strategische Investor", "stamm": "Ökonomisch", "abgrenzung": "Langzeit-Kalkül statt Repräsentation"},
    "T4": {"name": "Der materielle Ästhet", "stamm": "Ökonomisch", "abgrenzung": "Repräsentation statt Stabilität"},
    "T5": {"name": "Der funktionale Konservative", "stamm": "Ökonomisch", "abgrenzung": "Stabilitäts-Sicherung statt Expansion"},
    "T6": {"name": "Der klassische Intellektuelle", "stamm": "Kulturell", "abgrenzung": "Asketische Distanz statt Grenzüberschreitung"},
    "T7": {"name": "Der Avantgardist", "stamm": "Kulturell", "abgrenzung": "Grenzüberschreitung statt Tradition"},
    "T8": {"name": "Der Experte", "stamm": "Kulturell", "abgrenzung": "Wissens-Monopol statt Distanz"},
    "T9": {"name": "Der Bildungs-Bürger", "stamm": "Kulturell", "abgrenzung": "Tradition statt Wissens-Monopol"},
    "T10": {"name": "Der reflektierte Autodidakt", "stamm": "Kulturell", "abgrenzung": "Institutionelle Distanz statt Asketik"},
    "T11": {"name": "Der Netzwerker", "stamm": "Sozial", "abgrenzung": "Zirkulation statt Habitus-Angleichung"},
    "T12": {"name": "Der Mimikry-Aufsteiger", "stamm": "Sozial", "abgrenzung": "Habitus-Angleichung statt Transaktion"},
    "T13": {"name": "Der Broker", "stamm": "Sozial", "abgrenzung": "Transaktions-Gestik statt Regel-Manipulation"},
    "T14": {"name": "Der prekäre Improvisierer", "stamm": "Sozial", "abgrenzung": "Situations-Zwang statt Zirkulation"},
    "T15": {"name": "Der System-Spieler", "stamm": "Sozial", "abgrenzung": "Regel-Manipulation statt Situations-Zwang"}
}

st.title("Soziologische Maschine: Demystifizierungs-Apparat")

# Input
uploaded_file = st.file_uploader("Bild laden...")
hexis = st.text_input("Hexis (Haltung):")
doxa = st.text_input("Doxa (Kontext):")
wahl = st.selectbox("Typus-Zuweisung:", [f"{k}: {v['name']}" for k, v in TAXONOMY.items()])

if st.button("Analysieren"):
    if uploaded_file: st.image(uploaded_file, use_container_width=True)
    
    typ_id = wahl.split(":")[0]
    typ_daten = TAXONOMY[typ_id]
    
    # Grid-Visualisierung (Schwarz/Grau)
    cols = st.columns(5)
    for i, (k, v) in enumerate(TAXONOMY.items()):
        with cols[i % 5]:
            if k == typ_id:
                st.markdown(f"**<span style='color:black'>{k}: {v['name']}</span>**", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:grey'>{k}: {v['name']}</span>", unsafe_allow_html=True)
    
    # Kontrastive Begründung
    st.write("---")
    st.write(f"### Analyse-Begründung für {typ_id}")
    st.write(f"**Habitus-Indikator:** '{hexis}' im Kontext '{doxa}'.")
    st.write(f"**Stammes-Logik ({typ_daten['stamm']}):** Dieser Typus zeichnet sich durch {typ_daten['abgrenzung']} aus.")
    st.write(f"**Abgrenzung:** {typ_id} ist spezifisch, da er sich gegen die anderen Typen des Stammes {typ_daten['stamm']} abhebt, indem er das Merkmal '{typ_daten['abgrenzung']}' priorisiert.")
