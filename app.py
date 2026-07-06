import streamlit as st
from openai import OpenAI
import base64

# Initialisierung des Clients
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

def demystifiziere_bild(image_file):
    base64_image = encode_image(image_file)
    
    prompt = """
    Analysiere das Bild streng soziologisch nach dem 'Handbuch'.
    Liefere die Antwort ausschließlich im JSON-Format mit diesen vier Schlüsseln:
    - tA (Aussage): Beschreibung der materiellen Form/des Settings.
    - lA (Bedeutung): Analyse der Hexis und Doxa.
    - sA (Sachverhalt): Abgleich Hexis vs. Feld-Norm.
    - zA (Zuweisung): Soziale Verortung des Akteurs.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}
        ],
        response_format={ "type": "json_object" }
    )
    return response.choices[0].message.content

# Interface-Logik bleibt stabil
# ... (Aufruf von demystifiziere_bild innerhalb des Buttons)
