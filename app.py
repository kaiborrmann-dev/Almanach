import streamlit as st
from PIL import Image
import base64
import io
import json
from openai import OpenAI

# -----------------------------------------------------------------------------
# KONFIGURATION & UI-SETUP
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Affinités Électives | Habitus-Analyse", 
    page_icon="✨", 
    layout="wide"
)

# API Client initialisieren
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.warning("Bitte hinterlege deinen API-Key in den Streamlit-Secrets.")
    st.stop()

st.title("✨ Affinités Électives")
st.markdown("""
**Die Architektur der Anziehung entdecken.** Diese Anwendung analysiert die körperliche Disposition (*Hexis*) und den kulturellen Stil, 
um die objektive soziale Position sichtbar zu machen. Psychologisierende Kategorien werden ignoriert.
""")
st.divider()

# -----------------------------------------------------------------------------
# KI-ANALYSE FUNKTIONEN
# -----------------------------------------------------------------------------
def encode_image(image):
    """Wandelt das Bild für die API in Base64 um."""
    buffered = io.BytesIO()
    # Konvertiere in RGB, falls es ein PNG mit Transparenz ist
    if image.mode != "RGB":
        image = image.convert("RGB")
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def analyze_habitus_with_ai(image):
    """
    Sendet das Bild an die Vision-KI mit strikten soziologischen Vorgaben
    entsprechend der Generativen Prädikaten-Matrix.
    """
    base64_image = encode_image(image)
    
    system_prompt = """
    Du bist ein soziologischer Analyst. Wende strikt die Konzepte von Bourdieu an. 
    Analysiere das Bild und generiere eine Diagnose basierend auf:
    1. Raum-Hexis (Körperliche Disposition im Raum)
    2. Blick-Regime (Visuelle Interaktion mit dem Feld)
    3. Sartoriale Distinktion (Kleidungscodes, Dissonanz oder Konformität)
    
    Keine psychologisierenden Begriffe. Nutze Vokabular wie Doxa, Hexis, Hyperkorrektur, kulturelles Kapital.
    Antworte AUSSCHLIESSLICH mit einem validen JSON-Objekt im folgenden Format:
    {
        "hexis": "kurze Analyse",
        "blick": "kurze Analyse",
        "distinktion": "kurze Analyse",
        "synthese": "Zusammenfassende soziologische Diagnose"
    }
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analysiere den Habitus dieses Akteurs:"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        temperature=0.3
    )
    
    return json.loads(response.choices[0].message.content)

def evaluate_resonance_with_ai(data1, data2):
    """
    Übergibt die beiden extrahierten Prädikaten-Bündel an die KI, 
    um die strukturelle Isomorphie (Bedingungs-Schleife) zu berechnen.
    """
    system_prompt = """
    Du bist ein soziologischer Analyst. Führe die Bedingungs-Schleife aus.
    Vergleiche zwei Habitus-Profile auf ihre strukturelle Isomorphie. 
    Achte strikt auf die Abstraktions-Falle: Keine psychologischen Vergleiche. 
    Analysiere ausschließlich die Kompatibilität der habituellen Dispositionen (Raum-Hexis, Blick, Distinktion).
    Beurteile die Wahrscheinlichkeit für 'Amor fati'
