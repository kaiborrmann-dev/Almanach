import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io

# API-Key aus den Streamlit-Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def get_image_base64(image):
    buffered = io.BytesIO()
    # Bild verkleinern, damit die API nicht überlastet wird
    image.thumbnail((1024, 1024))
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def analysiere_habitus_mit_handbuch(image_base64):
    handbuch_prompt = """
    Du bist ein Experte für soziologische Demystifizierung nach Pierre Bourdieu. 
    Analysiere das Bild basierend auf dem Handbuch: 
    1. Erkenne die Hexis (Körperhaltung/Stil).
    2. Bestimme die Doxa (die gesetzten Tatsachen ↓A und die definierte Absenz ↑A).
    3. Ordne das Bild einem der 15 Habitus-Archetypen zu.
    4. Achte strikt auf Modul 14 (keine Abstraktions-Falle!) und Modul 15 (Bedingungs-Schleife).
    Antworte präzise und soziologisch fundiert.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": handbuch_prompt},
            {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}]}
        ]
    )
    return response.choices[0].message.content

st.title("Soziologischer Habitus-Demonstrator")

# Kamera-Input für mobile Nutzer
uploaded_file = st.camera_input("Kamera für die Demystifizierung öffnen")

if uploaded_file is not None:
    # Das Bild in ein PIL-Format konvertieren
    image = Image.open(uploaded_file)
    st.image(image, caption='Analysiertes Bild', use_container_width=True)
    
    if st.button('Soziologisch demystifizieren'):
        with st.spinner('Analysiere Habitus und Doxa...'):
            try:
                base64_image = get_image_base64(image)
                resultat = analysiere_habitus_mit_handbuch(base64_image)
                st.success("Analyse abgeschlossen:")
                st.write(resultat)
            except Exception as e:
                st.error(f"Ein Fehler ist aufgetreten: {e}")
