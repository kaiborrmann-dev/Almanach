import streamlit as st

# Die 15 Archetypen-Datenbank mit definierter Stammes-Logik
ARCHETYPEN = {
    "T1": {"name": "Der kalkulierte Erbe", "kapital": "Ökonomisch", "fokus": "Konservierung von Besitz"},
    "T2": {"name": "Der Markt-Akteur", "kapital": "Ökonomisch", "fokus": "Aggressive Expansion"},
    "T3": {"name": "Der strategische Investor", "kapital": "Ökonomisch", "fokus": "Langzeit-Kalkül"},
    "T4": {"name": "Der materielle Ästhet", "kapital": "Ökonomisch", "fokus": "Repräsentativer Konsum"},
    "T5": {"name": "Der funktionale Konservative", "kapital": "Ökonomisch", "fokus": "Stabilitäts-Sicherung"},
    "T6": {"name": "Der klassische Intellektuelle", "kapital": "Kulturell", "fokus": "Asketische Distanz"},
    "T7": {"name": "Der Avantgardist", "kapital": "Kulturell", "fokus": "Grenzüberschreitung"},
    "T8": {"name": "Der Experte", "kapital": "Kulturell", "fokus": "Wissens-Monopol"},
    "T9": {"name": "Der Bildungs-Bürger", "kapital": "Kulturell", "fokus": "Traditions-Verwaltung"},
    "T10": {"name": "Der reflektierte Autodidakt", "kapital": "Kulturell", "fokus": "Institutionelle Distanz"},
    "T11": {"name": "Der Netzwerker", "kapital": "Sozial", "fokus": "Zirkulation von Kontakten"},
    "T12": {"name": "Der Mimikry-Aufsteiger", "kapital": "Sozial", "fokus": "Habitus-Angleichung"},
    "T13": {"name": "Der Broker", "kapital": "Sozial", "fokus": "Transaktions-Gestik"},
    "T14": {"name": "Der prekäre Improvisierer", "kapital": "Sozial", "fokus": "Situations-Zwang"},
    "T15": {"name": "Der System-Spieler", "kapital": "Sozial", "fokus": "Regel-Manipulation"}
}

st.title("Soziologische Maschine: Demystifizierungs-Apparat")

# 1. Input-Sektion
uploaded_file = st.file_uploader("Bild laden (Börse, Szene, Habitus-Probe):", type=["jpg", "png", "webp"])
hexis = st.text_input("Hexis (Beobachtete Haltung):")
doxa = st.text_input("Doxa (Beobachteter Kontext):")
wahl = st.selectbox("Einordnung (Wähle den passenden Typ):", [f"{k}: {v['name']}" for k, v in ARCHETYPEN.items()])

if st.button("Analysieren"):
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)
    
    typ_id = wahl.split(":")[0]
    typ_daten = ARCHETYPEN[typ_id]
    
    st.subheader("Analyse-Ergebnis")
    
    # 2. Visualisierung des Baums (Schwarz/Grau-Logik)
    cols = st.columns(5)
    for i, (k, v) in enumerate(ARCHETYPEN.items()):
        with cols[i % 5]:
            if k == typ_id:
                st.markdown(f"**<span style='color:black'>{k}: {v['name']}</span>**", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:grey'>{k}: {v['name']}</span>", unsafe_allow_html=True)
    
    # 3. Kontrastive Begründung
    st.write("---")
    st.write(f"### Analyse-Begründung für {typ_id}: {typ_daten['name']}")
    st.write(f"**Habitus-Indikator:** Das Subjekt zeigt eine '{hexis}'-Haltung im Kontext '{doxa}'.")
    st.write(f"**Stammes-Logik ({typ_daten['kapital']}):** Dieser Typus ist definiert durch den Fokus auf '{typ_daten['fokus']}'.")
    
    st.write(f"**Abgrenzung:** {typ_id} ist nicht mit den anderen Typen des {typ_daten['kapital']}-Stammes identisch, da diese andere Schwerpunkte setzen (z. B. {', '.join([v['fokus'] for k, v in ARCHETYPEN.items() if v['kapital'] == typ_daten['kapital'] and k != typ_id][:3])} ...).")
