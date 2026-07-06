import streamlit as st
import random

def analysiere_bild(file):
    # Simulation einer Merkmals-Extraktion (statt fester Texte)
    # Hier würde in einem vollen System die Bild-KI die Parameter erkennen
    score = random.random() # Wir simulieren einen variablen Wert für jedes Bild
    
    if score > 0.5:
        return {
            "Hexis": "Ausgeprägte habituelle Souveränität; entspannte Raumaneignung.",
            "Doxa": "Sichere Reproduktion der Feldnormen ohne sichtbare Anstrengung.",
            "Habitus": "Kongruente Integration in das soziale Feld (Typ: Etabliert)."
        }
    else:
        return {
            "Hexis": "Habituelle Irritation; Anzeichen von Anspannung oder Diskrepanz.",
            "Doxa": "Bruch der selbstverständlichen Feld-Codes; 'Pädanterie' erkennbar.",
            "Habitus": "Strukturelle Hysteresis; Zeichen eines Misfit-Status."
        }

def main():
    st.title("Soziologische Analyse")
    uploaded_file = st.file_uploader("Bild hochladen", type=['jpg'])
    
    if uploaded_file:
        st.image(uploaded_file)
        if st.button("Analyse starten"):
            ergebnis = analysiere_bild(uploaded_file)
            for kategorie, inhalt in ergebnis.items():
                st.write(f"### {kategorie}")
                st.write(inhalt)

if __name__ == "__main__":
    main()
