import streamlit as st
import openai

# 1. DAS MODELL: Der logische Filter nach dem Handbuch
def soziologische_analyse(image_bytes):
    prompt = """
    Analysiere das Bild als soziologische Struktur.
    Bewerte strikt anhand dieser drei Kategorien:
    
    1. Hexis: Identifiziere die körperliche Manifestation (Tonus, Raumaneignung).
    2. Doxa: Identifiziere die unhinterfragte Selbstverständlichkeit/Normen.
    3. Habitus: Ordne das Resultat in die soziale Struktur ein (z.B. Kongruenz vs. Hysteresis).
    
    Antworte in einem präzisen JSON-Format.
    """
    
    # Hier erfolgt der Aufruf an die KI mit dem festen strukturellen Framework
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": [{"type": "text", "text": prompt}, ...]}],
        response_format={ "type": "json_object" }
    )
    return response.json()

# 2. DAS INTERFACE: Streamlit
def main():
    st.title("Soziologische Demystifizierung - Prod")
    uploaded_file = st.file_uploader("Bild laden", type=['jpg'])
    
    if uploaded_file:
        if st.button("Analyse starten"):
            # Die Analyse wird durch das Handbuch-Framework erzwungen
            resultat = soziologische_analyse(uploaded_file)
            st.json(resultat)
