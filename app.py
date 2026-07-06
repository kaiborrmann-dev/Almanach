import streamlit as st

def main():
    st.title("Soziale Distanz-Mapping")
    
    files = st.file_uploader("Akteure hochladen", accept_multiple_files=True)
    
    if len(files) == 2:
        if st.button("Distanz berechnen"):
            # Analysiere Akteur 1 und Akteur 2
            res1 = demystifiziere_bild(files[0]) # Unsere bisherige Funktion
            res2 = demystifiziere_bild(files[1])
            
            st.write("### Analyse-Vergleich")
            col1, col2 = st.columns(2)
            col1.json(res1)
            col2.json(res2)
            
            # Berechnung der Distanz
            distanz = berechne_soziale_distanz(res1, res2)
            st.metric(label="Soziale Distanz-Einheiten", value=distanz)
            
            st.info("Eine hohe Distanz deutet auf habituelle Divergenz hin.")

if __name__ == "__main__":
    main()
