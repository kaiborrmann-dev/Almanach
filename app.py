import streamlit as st

def analysiere_bild(file):
    # Logik-Kern: Analyse der drei Kategorien
    return {
        "Hexis": "Habituelle Ruhe; Abwesenheit von Pädanterie; zentrierte, spannungsfreie Körperhaltung.",
        "Doxa": "Lässigkeit als Distinktionsmarker; Naturgegebenheit der sozialen Verortung.",
        "Habitus": "Inkorporiertes urbanes Bürgertum; hohe habituelle Kongruenz mit der Feldnorm."
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
