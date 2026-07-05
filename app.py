import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io

# API-Key aus den Streamlit-Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def get_image_base64(image):
    buffered = io.BytesIO()
    image.thumbnail((1024, 1024))
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def analysiere_habitus_mit_handbuch(image_base64):
    # Die bewährte Logik: Hexis/Doxa kombiniert mit der Strenge des Handbuchs
    handbuch_prompt = """
    Du bist der soziologische Analysator des 'Handbuchs'. 
    Führe eine radikale Demystifizierung des Bildes durch, indem du dich primär auf 
    die Hexis (Körperhaltung/Stil) und die Doxa (die gesetzten Tatsachen ↓A und die definierte Absenz ↑A) konzentrierst.
    
    Strukturiere deine Analyse strikt anhand der 10 Operatoren (tA, lA, sA, eA, ↓A, ↑A, mA, kA, pA, fA) und zA.
    Verhindere Modul 14 (Abstraktions-Falle) und Modul 15 (Bedingungs-Schleife).
    
    Dein Stil ist analytisch, scharf und orientiert an den soziologischen Standards von Koppetsch (K1, K2).
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
st.write("Wähle ein Foto aus, um den Habitus zu demystifizieren.")

uploaded_file = st.file_uploader("Foto auswählen...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Analysiertes Bild', use_container_width=True)
    
    if st.button('Soziologisch demystifizieren'):
        with st.spinner('Demystifizierung läuft...'):
            try:
                base64_image = get_image_base64(image)
                resultat = analysiere_habitus_mit_handbuch(base64_image)
                st.success("Ergebnis der soziologischen Analyse:")
                st.write(resultat)
            except Exception as e:
                st.error(f"Ein Fehler ist aufgetreten: {e}")
