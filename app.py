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
    
    system_prompt = (
        "Du bist ein soziologischer Analyst. Wende strikt die Konzepte von Bourdieu an. "
        "Analysiere das Bild und generiere eine Diagnose basierend auf: "
        "1. Raum-Hexis (Körperliche Disposition im Raum) "
        "2. Blick-Regime (Visuelle Interaktion mit dem Feld) "
        "3. Sartoriale Distinktion (Kleidungscodes, Dissonanz oder Konformität) "
        "Keine psychologisierenden Begriffe. Nutze Vokabular wie Doxa, Hexis, Hyperkorrektur, kulturelles Kapital. "
        "Antworte AUSSCHLIESSLICH mit einem validen JSON-Objekt im folgenden Format: "
        '{"hexis": "kurze Analyse", "blick": "kurze Analyse", "distinktion": "kurze Analyse", "synthese": "Zusammenfassende Diagnose"}'
    )
    
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
    system_prompt = (
        "Du bist ein soziologischer Analyst. Führe die Bedingungs-Schleife aus. "
        "Vergleiche zwei Habitus-Profile auf ihre strukturelle Isomorphie. "
        "Achte strikt auf die Abstraktions-Falle: Keine psychologischen Vergleiche. "
        "Analysiere ausschließlich die Kompatibilität der habituellen Dispositionen (Raum-Hexis, Blick, Distinktion). "
        "Beurteile die Wahrscheinlichkeit für 'Amor fati' und 'Complicité corporelle'. "
        "Antworte AUSSCHLIESSLICH mit einem validen JSON-Objekt in diesem Format: "
        '{"score": 85, "analyse": "Soziologische Begründung der Resonanz oder Dissonanz"}'
    )
    
    prompt_content = f"Profil 1:\n{json.dumps(data1, ensure_ascii=False)}\n\nProfil 2:\n{json.dumps(data2, ensure_ascii=False)}"
    
    response = client.chat.completions.create(
        model="gpt-4o", 
        response_format={"type": "json_object"},
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
    
    # 1. Bilder verarbeiten und analysieren
    for file in uploaded_files:
        try:
            img = Image.open(file)
            img.thumbnail((800, 800)) # Komprimierung, um API-Limits und Ladezeiten zu schonen
            
            with st.spinner(f"Analysiere Akteur '{file.name}'..."):
                analysis = analyze_habitus_with_ai(img)
                profiles.append({
                    "name": file.name,
                    "image": img,
                    "data": analysis
                })
        except Exception as e:
            st.error(f"Fehler bei der Analyse der Datei {file.name}: {e}")

    # 2. Profile nebeneinander darstellen
    if profiles:
        cols = st.columns(len(profiles))
        for idx, profile in enumerate(profiles):
            with cols[idx]:
                st.image(profile["image"], caption=f"Akteur {idx+1}", use_container_width=True)
                st.success(f"**Diagnose:** {profile['data'].get('synthese', 'Keine Synthese verfügbar')}")
                
                st.markdown("**🧭 Raum-Hexis**")
                st.write(profile['data'].get('hexis', ''))
                
                st.markdown("**👁️ Blick-Regime**")
                st.write(profile['data'].get('blick', ''))
                
                st.markdown("**🧥 Distinktion**")
                st.write(profile['data'].get('distinktion', ''))

    # -----------------------------------------------------------------------------
    # 3. RESONANZ-ABGLEICH (BEDINGUNGS-SCHLEIFE)
    # -----------------------------------------------------------------------------
    if len(profiles) == 2:
        st.divider()
        st.subheader("💞 Strukturelle Resonanz (Vergleich der Profile)")
        
        with st.spinner("Berechne Wahrscheinlichkeit für Amor fati und Complicité corporelle..."):
            try:
                resonance_result = evaluate_resonance_with_ai(profiles[0]["data"], profiles[1]["data"])
                score = resonance_result.get("score", 0)
                analyse_text = resonance_result.get("analyse", "Keine Analyse verfügbar.")
                
                st.progress(score / 100)
                
                if score >= 85:
                    st.success(f"**Hohe Isomorphie ({score}% Resonanz):** {analyse_text}")
                elif score >= 65:
                    st.warning(f"**Partielle Resonanz ({score}% Resonanz):** {analyse_text}")
                else:
                    st.error(f"**Habituelle Dissonanz ({score}% Resonanz):** {analyse_text}")
                    
            except Exception as e:
                st.error(f"Fehler bei der Berechnung der Resonanz: {e}")
