import numpy as np
import streamlit as st

st.title("Habituelle Milieu-Passung")
st.write("Strukturiertes Matching über Distanz-Metrik (Mismatch-Bestrafung).")

# Beispiel-Profile als Vektoren: [KldB (skaliert), Bildung (1-5), Kulturelles Kapital (1-5), Ökonomischer Index (1-5)]
# Hinweis: KldB-Werte zur besseren Vergleichbarkeit im Vektor kleiner skaliert oder als separate Kategorie behandelt.
PROFILE_DB = {
    "Anna": {"vektor": [2.1, 5, 4, 3], "milieu": "Akademisch-kulturell"},
    "Bernd": {"vektor": [7.1, 2, 1, 4], "milieu": "Technisch-gewerblich"},
    "Clara": {"vektor": [2.1, 5, 5, 4], "milieu": "Akademisch-kulturell"},
    "David": {"vektor": [5.1, 3, 2, 2], "milieu": "Dienstleistungsorientiert"},
}

def berechne_milieu_passung(vektor_a, vektor_b):
    """Berechnet einen Passungs-Score (0 bis 1) basierend auf der euklidischen Distanz.
    Je größer der Abstand, desto geringer die Passung."""
    a = np.array(vektor_a, dtype=float)
    b = np.array(vektor_b, dtype=float)
    
    # Euklidischer Abstand
    abstand = np.linalg.norm(a - b)
    
    # In einen Score zwischen 0 und 1 transformieren (1 = identisch, sinkt bei Abstand)
    # Der Teiler (z.B. 10.0) skaliert die Empfindlichkeit der Abweichung
    score = 1.0 / (1.0 + 0.3 * abstand)
    return float(score)

def finde_matches(ziel_name, db):
    if ziel_name not in db:
        return []

    ziel_vektor = db[ziel_name]["vektor"]
    ergebnisse = []

    for name, daten in db.items():
        if name == ziel_name:
            continue

        score = berechne_milieu_passung(ziel_vektor, daten["vektor"])
        ergebnisse.append({
            "name": name, 
            "milieu": daten["milieu"], 
            "passung": round(score, 3)
        })

    ergebnisse = sorted(ergebnisse, key=lambda x: x["passung"], reverse=True)
    return ergebnisse

auswahl = st.selectbox("Wähle ein Profil für das Matching:", list(PROFILE_DB.keys()))

if auswahl:
    st.subheader(f"Profil: {auswahl} ({PROFILE_DB[auswahl]['milieu']})")
    st.write("Vektor-Parameter:", PROFILE_DB[auswahl]["vektor"])

    if st.button("Passende Milieus berechnen"):
        matches = finde_matches(auswahl, PROFILE_DB)
        
        st.markdown("### Top-Matches (Nach Distanz)")
        for m in matches:
            st.write(f"- **{m['name']}** | Milieu: {m['milieu']} | Passungs-Score: `{m['passung']}`")
