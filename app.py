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

# API Client initialisieren (Holt sich den Key aus den Streamlit Secrets oder Umgebungsvariablen)
# Für lokale Tests kannst du direkt client = OpenAI(api_key="DEIN_API_KEY") nutzen
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.warning("Bitte API-Key in den Streamlit-Secrets hinterlegen.")
    st.stop()

st.title("✨ Affinités Électives")
st.markdown("""
**Die Architektur der Anziehung entdecken.** Diese Anwendung analysiert die körperliche Disposition (*Hexis*) und den kulturellen Stil aus, 
um die objektive soziale Position sichtbar zu machen.
""")
st.divider()

# -----------------------------------------------------------------------------
# KI-ANALYSE FUNKTION (Die echte Anbindung)
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
    
    # Der System-Prompt zwingt die KI in unser theoretisches Korsett
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
        "synthese": "Zusammenfassende soziologische Diagnose (z.B. Kulturkapitalistisch fundierter Habitus)"
    }
    """
    
    response = client.chat.completions.create(
        model="gpt-4o", # oder ein anderes Vision-fähiges Modell
        response_format={ "type": "json_object" },
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analysiere den Habitus dieses Akteurs:"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        temperature=0.3 # Niedrige Temperatur für analytische Präzision
    )
    
    # JSON-Antwort der KI verarbeiten
    result_text = response.choices[0].message.content
    return json.loads(result_text)

# -----------------------------------------------------------------------------
# APP-LOGIK (UPLOAD & DARSTELLUNG)
# -----------------------------------------------------------------------------
st.markdown("### 📸 Profil-Analyse starten")
uploaded_files = st.file_uploader(
    "Visuelle Termini hochladen", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 2:
        st.warning("Bitte laden Sie maximal zwei Bilder für einen direkten Resonanz-Abgleich hoch.")
        uploaded_files = uploaded_files[:2]

    profiles = []
    
    # Echte Analyse durchführen
    for file in uploaded_files:
        img = Image.open(file)
        # Bild komprimieren, um API-Kosten/Zeit zu sparen
        img.thumbnail((800, 800)) 
        
        with st.spinner(f"Analysiere Akteur {file.name} über die Vision-API..."):
            try:
                analysis = analyze_habitus_with_ai(img)
                profiles.append({
                    "name": file.name,
                    "image": img,
                    "data": analysis
                })
            except Exception as e:
                st.error(f"Fehler bei der API-Analyse: {e}")

    # Darstellung der Ergebnisse
    cols = st.columns(len(profiles))
    for idx, profile in enumerate(profiles):
        with cols[idx]:
            st.image(profile["image"], caption=f"Akteur {idx+1}", use_container_width=True)
            st.success(f"**Diagnose:** {profile['data'].get('synthese', '')}")
            
            st.markdown("**🧭 Raum-Hexis**")
            st.write(profile['data'].get('hexis', ''))
            
            st.markdown("**👁️ Blick-Regime**")
            st.write(profile['data'].get('blick', ''))
            
            st.markdown("**🧥 Distinktion**")
            st.write(profile['data'].get('distinktion', ''))

    # -----------------------------------------------------------------------------
    # RESONANZ-ABGLEICH (MODUL 15: BEDINGUNGS-SCHLEIFE)
    # -----------------------------------------------------------------------------
    if len(profiles) == 2:
        st.divider()
        st.subheader("💞 Strukturelle Resonanz (Isomorphie-Prüfung)")
        st.info("Das System hat zwei Profile erfasst. Die strukturelle Isomorphie der extrahierten Prädikate wird nun abgeglichen...")
        # Hier würde dann die logische Evaluierung der beiden JSONs erfolgen
