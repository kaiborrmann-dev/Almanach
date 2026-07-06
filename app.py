import streamlit as st
import json

# 1. Die Analyse-Funktion (Die Engine)
def demystifiziere_bild(image_file):
    # Simulation der API-Antwort für das Interface-Testing
    # Sobald das läuft, ersetzen wir das return durch den OpenAI-API-Aufruf
    return {
        "tA": "Materielle Form: Urbanes Setting.",
        "lA": "Hexis: Kongruent.",
        "sA": "Abgleich: Keine Hysteresis.",
        "zA": "Etabliert"
    }

# 2. Die Distanz-Berechnung
def berechne_soziale_distanz(res1, res2):
    # Distanz-Logik: Vergleich der zA-Zuweisung
    return 0 if res1["zA"] == res2["zA"] else 1

def main():
    st.title("Soziale Distanz-Mapping")
    
    files = st.file_uploader("Akteure hochladen", accept_multiple_files=True, type=['jpg'])
    
    if files and len(files) == 2:
        if st.button("Distanz berechnen"):
            with st.spinner('Demystifizierung läuft...'):
                # Hier wird die Funktion nun korrekt aufgerufen
                res1 = demystifiziere_bild(files[0])
                res2 = demystifiziere_bild(files[1])
                
                col1, col2 = st.columns(2)
                col1.json(res1)
                col2.json(res2)
                
                distanz = berechne_soziale_distanz(res1, res2)
                st.metric(label="Soziale Distanz-Einheiten", value=distanz)
    elif files:
        st.write("Bitte genau 2 Bilder hochladen.")

if __name__ == "__main__":
    main()
