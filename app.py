import streamlit as st
from PIL import Image
import time
import random

# Konfiguration für ein leichtes, freundliches UI
st.set_page_config(
    page_title="Affinités Électives | Habitus-Analyse", 
    page_icon="✨", 
    layout="centered"
)

# Positives, einladendes Framing der App
st.title("✨ Affinités Électives")
st.markdown("""
**Die Architektur der Anziehung entdecken.**  
Diese Anwendung nutzt soziologische Strukturanalysen, um jenseits von psychologischen Tests echte *Resonanz* sichtbar zu machen. 
Wir analysieren die nonverbale Sprache, die körperliche Disposition (*Hexis*) und den kulturellen Stil, um die objektive soziale Position sichtbar zu machen – die Grundlage für *Amor fati* und tiefe, dauerhafte Verbindungen.
""")

st.divider()

# Leichtgewichtiges Interface für den Upload
uploaded_file = st.file_uploader("Laden Sie ein Foto hoch, um die dynamische Habitus-Struktur zu analysieren:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    st.image(image, caption="Ihr visuelles Profil", use_container_width=True)
    
    st.divider()
    
    with st.spinner("Lese habituelle Dispositionen und soziale Codes aus..."):
        time.sleep(2) # Simuliert die API-Analyse des Bildes
        
        # Dynamische Simulation der "Generativen Prädikaten-Matrix"
        # In der echten App werden diese Werte durch eine Vision-KI aus dem Bild extrahiert
        raum_hexis = random.choice([
            "Expansive und entspannte Inanspruchnahme des Raumes. Zeigt eine natürliche Vertrautheit mit der Umgebung.",
            "Fokussierte und zentrierte Körperhaltung. Signalisiert eine dynamische, zielgerichtete Präsenz.",
            "Asymmetrische, ruhende Disposition. Weist auf eine souveräne Distanz zu starren Konventionen hin."
        ])
        
        blick_regime = random.choice([
            "Direkter, affektbefreiter Blick. Kommuniziert auf Augenhöhe, ohne Bestätigung einzufordern.",
            "Offener, aufmerksamer Blick. Zeigt eine hohe Empfänglichkeit für die Doxa des umgebenden Feldes.",
            "Reflektierter, leicht distanzierter Ausdruck. Markiert die Position des gelassenen Beobachters."
        ])
        
        sartoriale_distinktion = random.choice([
            "Subtiler Einsatz von kulturellem Kapital durch bewussten Verzicht auf laute Statussymbole.",
            "Ästhetisierte Codes und stilsichere Materialwahl, die eine klare Eigenständigkeit formulieren.",
            "Klassische Strukturierung mit feinen, individuellen Abweichungen von der Norm."
        ])
        
        habitus_synthese = random.choice([
            "Kulturkapitalistisch fundierter, souveräner Habitus mit hoher Feld-Dominanz.",
            "Aufstrebender, dynamischer Habitus mit starker Anpassungsfähigkeit an urbane Kontexte.",
            "Intellektualisierter Habitus, der sich durch ästhetische Distinktion und doxische Sicherheit auszeichnet."
        ])

        # Ausgabe der dynamisch generierten Ergebnisse in einem sauberen Layout
        st.subheader("Ihre soziologische Signatur")
        
        st.info(f"**Die Diagnose:** {habitus_synthese}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🧭 Raum-Hexis")
            st.write(raum_hexis)
            
        with col2:
            st.markdown("### 👁️ Blick-Regime")
            st.write(blick_regime)
            
        with col3:
            st.markdown("### 🧥 Distinktion")
            st.write(sartoriale_distinktion)
            
        st.divider()
        
        st.subheader("💞 Resonanz & Matching")
        st.markdown("""
        Um das Potenzial für *Complicité corporelle* und instinktives Erkennen zu ermitteln, 
        benötigt das System ein zweites Profil. Der logische Abgleich erfolgt strikt über die 
        strukturelle Isomorphie der hier ermittelten *Hexis*-Parameter.
        """)
        
        if st.button("Zweites Profil für Resonanz-Abgleich hochladen"):
            st.warning("Diese Funktion ist in der Lightweight-Demo noch nicht freigeschaltet. Bitte implementieren Sie die Bild-Datenbank-Anbindung.")
