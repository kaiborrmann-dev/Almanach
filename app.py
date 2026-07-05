import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io

# API-Key aus den Streamlit-Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def get_image_base64(image):
    buffered = io.BytesIO()
    # Bild-Effizienz für die API
    image.thumbnail((1024, 1024))
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def analysiere_habitus_mit_handbuch(image_base64):
    # Gehärteter System-Prompt zur Sicherung der Konsistenz
    handbuch_prompt = """
    Du bist der soziologische Analysator des 'Handbuchs'. Deine Aufgabe ist die radikale Demystifizierung des Bild-Inputs.
    Wende bei jeder Analyse zwingend und explizit folgende 10 Operatoren an:
    1. tA (Aussage): Identität der materiellen Form.
    2. lA (Bedeutung): Systemischer Sinngehalt.
    3. sA (Sachverhalt): Referenz zur Außenwelt.
    4. eA (Wahrheitswert): Korrespondenz-Status.
    5. ↓A (Tatsache): Präsenz der sozialen Doxa.
    6. ↑A (Untatsache): Explizite Auslassungen.
    7. mA (Modus): Soziale Aktion.
    8. kA (Kontext): Rahmen-Zugehörigkeit.
    9. pA (Perspektive): Beobachter-Relativierung.
    10. fA (Finalität): Zweck der Inszenierung.
    11. zA (neuer Operator): Zusätzliche soziologische Dimension.
    
    Verhindere strikt Modul 14 (Abstraktions-Falle) und Modul 15 (Bedingungs-Schleife). 
    Antworte in einem präzisen, analytischen Stil (orientiert an K1/K2 von Koppetsch). 
    Jede Antwort MUSS diese Operatoren als Strukturvorgabe nutzen.
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
st.write("Wähle ein Foto aus deiner Galerie, um den Habitus nach dem Handbuch zu demystifizieren.")

# Galerie-Upload (Stabil und ohne Kamera-Berechtigungs-Hürden)
uploaded_file = st.file_uploader("Foto auswählen...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Analysiertes Bild', use_container_width=True)
    
    if st.button('Soziologisch demystifizieren'):
        with st.spinner('Analysiere Habitus und Doxa nach dem Handbuch...'):
            try:
                base64_image = get_image_base64(image)
                resultat = analysiere_habitus_mit_handbuch(base64_image)
                st.success("Demystifizierung abgeschlossen:")
                st.write(resultat)
            except Exception as e:
                st.error(f"Ein Fehler ist aufgetreten: {e}")
