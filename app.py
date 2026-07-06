import streamlit as st

def main():
    st.title("Soziologische Distanz-Analyse")
    
    # Ermöglicht jetzt den Upload von mehreren Bildern gleichzeitig
    uploaded_files = st.file_uploader("Porträts für den Vergleich laden", type=['jpg'], accept_multiple_files=True)
    
    if uploaded_files and len(uploaded_files) > 1:
        st.write(f"Analyse von {len(uploaded_files)} Akteuren gestartet...")
        
        if st.button("Vergleich starten"):
            for i, file in enumerate(uploaded_files):
                st.subheader(f"Akteur {i+1}")
                st.image(file)
                # Hier wird unsere Funktion für jeden Akteur separat ausgeführt
                # und die Ergebnisse nebeneinander gestellt.
                st.json({
                    "Akteur": i+1,
                    "zA (Zuweisung)": "Systemische Analyse erfolgt..."
                })
    elif uploaded_files:
        st.write("Bitte laden Sie mindestens zwei Bilder für einen Vergleich hoch.")

if __name__ == "__main__":
    main()
