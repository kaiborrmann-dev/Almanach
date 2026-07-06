import streamlit as st

# Die 15 Prädikaten-Systeme (T1-T15) mit Stammes-Logik für die Begründung
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

# --- KÜNSTLICHE INTELLIGENZ (VISION-Schnittstelle) ---
def analysiere_bild_mit_ki(image_file):
    """
    Hier wird das Bild an ein multimodales Modell (z.B. Vision API) gesendet.
    Die Maschine übernimmt die soziologische Phänomenologie vollständig.
    """
    # DUMMY-RETURN zur Simulation des API-Outputs für das GitHub-Repo:
    return {
        "hexis": "habituelle Konzentration und gestische Expansions-Bereitschaft",
        "doxa": "ein hochkompetitiver, ökonomisch codierter Raum",
        "typ_id": "T2"
    }

# --- FRONTEND ---
st.title("Soziologische Maschine: Demystifizierungs-Apparat")
st.write("Laden Sie ein Bild hoch. Die Maschine extrahiert Hexis und Doxa und deduziert den Habitus-Typus autonom.")

# EINZIGER INPUT: Das Bild
uploaded_file = st.file_uploader("Bild laden...", type=["jpg", "png", "webp"])

if uploaded_file is not None:
    st.image(uploaded_file, use_container_width=True)
    
    with st.spinner('Maschine scannt das Bild nach soziologischen Prädikaten...'):
        # 1. Bild geht an die Vision-KI
        analyse_ergebnis = analysiere_bild_mit_ki(uploaded_file)
        
        typ_id = analyse_ergebnis["typ_id"]
        typ_daten = TAXONOMY[typ_id]
        
        st.subheader("Deduktions-Ergebnis")
        
        # 2. Visualisierung (Schwarz/Grau)
        cols = st.columns(5)
        for i, (k, v) in enumerate(TAXONOMY.items()):
            with cols[i % 5]:
                if k == typ_id:
                    st.markdown(f"**<span style='color:black'>{k}: {v['name']}</span>**", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span style='color:grey'>{k}: {v['name']}</span>", unsafe_allow_html=True)
        
        # 3. Kontrastive Begründung aus der KI-Analyse
        st.write("---")
        st.write(f"### Analyse-Begründung für {typ_id}: {typ_daten['name']}")
        st.write(f"**Maschinelle Phänomenologie:** Die visuelle Analyse extrahiert als Hexis '{analyse_ergebnis['hexis']}' innerhalb der Doxa '{analyse_ergebnis['doxa']}'.")
        st.write(f"**Systemische Einordnung:** Dies verankert das Subjekt im Stamm '{typ_daten['stamm']}'.")
        
        # Abgrenzung
        andere_im_stamm = [f"{k} ({v['abgrenzung'].split(' statt ')[0]})" for k, v in TAXONOMY.items() if v['stamm'] == typ_daten['stamm'] and k != typ_id]
        st.write(f"**Abgrenzung:** {typ_id} ist spezifisch validiert, da das Bild das Merkmal '{typ_daten['abgrenzung']}' aufweist und somit die anderen Typen des Stammes ausschließt (welche auf {', '.join(andere_im_stamm)} basieren).")
