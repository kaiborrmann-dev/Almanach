import streamlit as st

st.set_page_config(page_title="Wahlverwandtschafts-Finder", layout="centered")

st.title("❤️ Der Wahlverwandtschafts-Finder")
st.markdown("Echte Menschen, echte Selbstbeschreibungen – finde die resonanten Paare $P(xx)$.")

# Speicher für echte Profile in der Session
if "profiles" not in st.session_state:
    st.session_state["profiles"] = []

# --- 1. EINGABE: Echte Personen erzählen über sich ---
st.subheader("1. Trag dein Profil ein")
with st.form("user_input_form", clear_on_submit=True):
    name = st.text_input("Dein Name / Alias")
    bio = st.text_area("Erzähl etwas über dich (Was treibt dich an? Woran glaubst du? Was liebst du?):")
    submitted = st.form_submit_button("Profil abschicken")
    
    if submitted and name and bio:
        # Extrahiere signifikante Wörter als Merkmale/Prädikate aus dem Text (Filter für kurze Füllwörter)
        extracted_preds = set(word.lower().strip(".,!?;:()[]") for word in bio.split() if len(word) > 3)
        
        # Profil speichern
        st.session_state["profiles"].append({
            "id": name,
            "bio": bio,
            "preds": extracted_preds
        })
        st.success(f"Danke, {name}! Dein Profil wurde aufgenommen.")

st.divider()

# --- 2. AKTUELLER BESTAND ---
st.subheader("2. Eingetragene Personen im Raum")
profiles = st.session_state["profiles"]

if profiles:
    for p in profiles:
        with st.expander(f"👤 {p['id']}"):
            st.write(f"*„{p['bio']}“*")
            st.caption(f"Extrahierte Resonanz-Marker: {list(p['preds'])}")
else:
    st.info("Noch keine Profile eingetragen. Fülle oben das Formular aus!")

st.divider()

# --- 3. BERECHNUNG DER WAHLVERWANDTSCHAFTEN P(xx) ---
st.subheader("3. Ermittelte Paare P(xx)")

if len(profiles) >= 2:
    pairs = []
    n = len(profiles)
    
    # Paarbildung ohne künstliche Mengen (Pluralogischer Ansatz P(xx))
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = profiles[i], profiles[j]
            shared_resonances = p1["preds"].intersection(p2["preds"])
            
            # Bedingung für Wahlverwandtschaft: Mindestens eine inhaltliche Schnittmenge
            if len(shared_resonances) > 0:
                pairs.append((p1["id"], p2["id"], shared_resonances))
                
    if pairs:
        st.success(f"{len(pairs)} plurale Paare $P(xx)$ mit echter Resonanz gefunden:")
        for idx, (u1, u2, resonances) in enumerate(pairs, 1):
            st.write(f"**Paar {idx} P(xx):** `{u1}` ⟷ `{u2}`")
            st.caption(f"Gemeinsame Anknüpfungspunkte: {list(resonances)}")
            st.markdown("---")
    else:
        st.warning("Keine Überschneidungen in den Texten gefunden. Schreibt detaillierter über eure Leidenschaften!")
else:
    st.info("Es werden mindestens 2 Personen benötigt, um Paare $P(xx)$ zu bilden.")
