import streamlit as st
from PIL import Image
import os

# Die Logik unserer Analyse
def analysiere_habitus(image):
    # Hier wird später der API-Call zur KI mit unserem Handbuch integriert
    return "Soziologische Analyse: Das Bild zeigt eine klare Doxa der 'Urban Cultural Fluency'. Die Hexis ist durch eine hohe 'low-cost' Mühelosigkeit gekennzeichnet."

st.title("Soziologischer Habitus-Demonstrator")
st.write("Laden Sie ein Bild hoch, um die implizite Doxa und den Habitus-Archetyp zu demystifizieren.")

uploaded_file = st.file_uploader("Bild auswählen...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Analysiertes Bild', use_column_width=True)
    
    if st.button('Soziologisch demystifizieren'):
        with st.spinner('Extrahiere Doxa...'):
            resultat = analysiere_habitus(image)
            st.success(resultat)
            st.info("System-Hinweis: Analyse basiert auf den Operatoren des Handbuchs.")
