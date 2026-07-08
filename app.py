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
except:
    st.warning("Bitte API-Key in den Streamlit-Secrets hinterlegen.")
    st.stop()

st.title("✨ Affinités Électives")
st.markdown("""
**Die Architektur der Anziehung entdecken.** Diese Anwendung analysiert die körperliche Disposition (*Hexis*) und den kulturellen Stil, 
um die objektive soziale Position sichtbar zu machen.
""")
st.divider()

# -----------------------------------------------------------------------------
# KI-ANALYSE FUNKTIONEN (Die echte Anbindung)
# -----------------------------------------------------------------------------
def encode_image(image):
    """Wandelt das Bild für die API in Base64 um."""
    buffered = io.BytesIO()
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
        "hexis": "kurzer Text",
        "blick": "kurzer Text",
        "distinktion": "kurzer Text",
        "synthese": "Zusammenfassende soziologische Diagnose"
    }
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
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
    um die strukturelle Isomorphie (Modul 15) zu berechnen.
    """
    system_prompt = """
    Du bist ein soziologischer Analyst. Führe Modul 15 (Bedingungs-Schleife) aus.
    Vergleiche zwei Habitus-Profile auf ihre strukturelle Isomorphie. 
    Achte strikt auf Modul 14 (Abstraktions-Falle): Keine psychologischen Vergleiche. 
    Analysiere ausschließlich die Kompatibilität der habituellen Dispositionen (Raum-Hexis, Blick, Distinktion).
    Beurteile die Wahrscheinlichkeit für 'Amor fati' und 'Complicité corporelle'.
    
    Antworte AUSSCHLIESSLICH mit einem validen JSON-Objekt in diesem Format:
    {
        "score": 85,
        "analyse": "Soziologische Begründung der Resonanz oder Dissonanz"
    }
    """
    
    prompt_content = f"Profil 1:\n{json.dumps(data1, ensure_ascii=False)}\n\nProfil 2:\n{json.dumps(data2, ensure_ascii=False)}"
    
    response = client.chat.completions.create(
        model="gpt-4o", 
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_content}
        ],
        temperature=0.2 
    )
    
    return json.loads(response.choices[0].message.content)

# -----------------------------------------------------------------------------
# APP-LOGIK (UPLOAD & DARSTELLUNG)
# -----------------------------------------------------------------------------
st.markdown("### 📸 Profil-Analyse starten")

st.info("💡 **Hinweis:** Laden Sie hier einfach zwei Bilder hoch; unten finden Sie direkt einen soziologischen Vergleich der Profile.")

uploaded_files = st.file_uploader(
    "Visuelle Termini (Bilder) auswählen", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 2:
        st.warning("Bitte laden Sie maximal zwei Bilder für einen direkten Resonanz-Abgleich hoch.")
        uploaded_files = uploaded_files[:2]

    profiles = []
    
    # Bilder analysieren
    for file in uploaded_files:
        img = Image.open(file)
        img.thumbnail((800, 800)) # Komprimierung
        
        with st.spinner(f"Analysiere Akteur '{file.name}'..."):
            try:
                analysis = analyze_habitus_with_ai(img)
                profiles.append({
                    "name": file.name,
                    "image": img,
                    "data": analysis
                })
            except Exception as e:
                st.error(f"Fehler bei der Analyse: {e}")

    # Profile darstellen
    cols = st.columns(len(profiles))
    for idx, profile in enumerate(profiles):
        with cols
