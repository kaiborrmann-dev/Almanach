import streamlit as st
from PIL import Image
import time

# Konfiguration der App
st.set_page_config(
    page_title="Soziologische Demystifizierung", 
    page_icon="👁️", 
    layout="wide"
)

# Header und theoretische Rahmung
st.title("Habitus-Analyse & Soziale Isomorphie")
st.markdown("""
Dieses System führt eine **soziologische Demystifizierung** durch. 
Es verzichtet auf psychologisierende Kategorien und analysiert stattdessen die unbewusste *Hexis corporelle* (körperliche Disposition) sowie visuelle *Distinktion*, um die objektive Position eines Akteurs im sozialen Raum zu bestimmen.
""")

st.divider()

# Datei-Upload
uploaded_file = st.file_uploader("Laden Sie ein Bild zur Habitus-Analyse hoch", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Layout in zwei Spalten
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.image(image, caption="Visuelles Analyseobjekt", use_container_width=True)
        
    with col2:
        st.subheader("Dynamische Habitus-Generierung")
        st.caption("Extraktion der materiell verankerten Codes...")
        
        # Simulation der analytischen Verarbeitung (Hier würde die KI/Vision-API greifen)
        with st.spinner("Analysiere Disposition und Doxa..."):
            time.sleep(2) 
            
            # 1. Mikroskopische Bausteine (Ohne formale Operatoren-Namen)
            st.markdown("### 1. Raum-Hexis")
            st.write("Die physische Disposition im Raum zeigt eine asymmetrische, entspannte Inanspruchnahme der Umgebung. Es liegt keine symmetrische Hyperkorrektur vor, was auf habituelle Sicherheit und Vertrautheit mit den Regeln des Feldes hindeutet.")
            
            st.markdown("### 2. Blick-Regime")
            st.write("Der direkte, affektbefreite Blick adressiert den Betrachter nicht als Bittsteller. Die Haltung gewährt visuelle Zugänglichkeit und markiert eine souveräne, distanzierte Position der Beobachtung.")
            
            st.markdown("### 3. Sartoriale Distinktion")
            st.write("Bewusste ästhetische Abweichung von strengen, ökonomischen Konventionen. Die Kombination spezifischer Muster und Accessoires (z.B. Brillenform) signalisiert inkorporiertes kulturelles Kapital und dient als Strategie der subtilen Abgrenzung.")
            
            st.divider()
            
            # 2. Die Synthese (Die soziologische Diagnose)
            st.subheader("Soziologische Verortung")
            st.success("**Kulturkapitalistisch fundierter, etablierter Habitus**")
            st.write("""
            Der Akteur markiert seine Position im sozialen Raum durch sartoriale Eigenständigkeit und physische Souveränität. 
            Es zeigen sich keine visuellen Indikatoren für *Hysteresis* (strukturellen Zweifel) oder einen deplatzierten Misfit-Status. 
            Die *Doxa* des umgebenden Feldes wird unhinterfragt und natürlich beherrscht.
            """)

        st.divider()
        
        # 3. Vorbereitung für Modul 14 & 15 (Resonanz)
        st.subheader("Soziologische Resonanz (Matching)")
        st.info("""
        **Systemhinweis zur Abstraktions-Falle:** Ein Abgleich von deklarierten Interessen oder psychologischen Profilen ist unzulässig. 
        Für eine Resonanz-Prüfung laden Sie bitte ein zweites visuelles Profil hoch. Das System iteriert dann in einer Bedingungs-Schleife, um die strukturelle Isomorphie der jeweiligen *Hexis* abzugleichen und die Wahrscheinlichkeit für *Amor fati* (Bejahung der sozialen Flugbahn) sowie *Complicité corporelle* zu ermitteln.
        """)
