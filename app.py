import streamlit as st

def main():
    st.title("Soziologische Demystifizierung - Alpha")
    
    # Sicherer Datei-Upload
    uploaded_file = st.file_uploader("Bild zur Analyse wählen", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Untersuchungsobjekt")
        
        # Manuelle Analyse-Simulation (Funktioniert sofort ohne API-Key-Risiko)
        if st.button("Analyse ausführen"):
            st.subheader("Strukturelle Diagnose")
            
            # Hier greift unser logisches Raster
            analyse = {
                "Hexis": "Ruhende Raumaneignung; kontrollierter Tonus.",
                "Doxa": "Konforme Inklusion in die bürgerliche Norm.",
                "Habitus": "Habituelle Kongruenz; keine Hysteresis."
            }
            
            for key, value in analyse.items():
                st.markdown(f"**{key}:** {value}")
            
            st.success("Operatoren-System: Analyse abgeschlossen.")

if __name__ == "__main__":
    main()
