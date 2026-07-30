import streamlit as st
import time

# --- SEITEN-SETUP ---
st.set_page_config(page_title="Milieu-Engine", layout="centered")

st.title("🧭 Milieu-Spiegel: Prototyp")
st.write("Beschreibe deinen Alltag, deine Werte und was dir im Leben wichtig ist. Die Engine verortet dich im gesellschaftlichen Koordinatensystem.")

# --- EINGABE-BEREICH ---
user_input = st.text_area(
    "Dein Text:", 
    height=150, 
    placeholder="Z. B. Ich arbeite als Lehrer, verbringe meine Wochenenden gern in der Natur oder auf Ausstellungen. Sicherheit ist mir weniger wichtig als Selbstverwirklichung..."
)

if st.button("Milieu analysieren"):
    if not user_input.strip():
        st.warning("Bitte gib zuerst einen Text ein.")
    else:
        with st.spinner("Analysiere Text..."):
            # Simuliere eine kleine Denkpause der "Engine"
            time.sleep(1.5) 
            
            # --- SIMPLE MOCK-ENGINE ---
            text = user_input.lower()
            x_orientierung = 5  
            y_lage = 5          
            
            # Kultur/Werte-Achse
            if any(word in text for word in ["natur", "selbstverwirklichung", "kunst", "kreativ", "offen"]):
                x_orientierung += 3
            if any(word in text for word in ["sicherheit", "familie", "tradition", "ordnung"]):
                x_orientierung -= 3
                
            # Soziale-Lage-Achse
            if any(word in text for word in ["management", "geld", "karriere", "führung"]):
                y_lage += 3
            if any(word in text for word in ["arbeitslos", "schulden", "stress", "hart"]):
                y_lage -= 3
                
            x_orientierung = max(0, min(10, x_orientierung))
            y_lage = max(0, min(10, y_lage))
            
            # --- AUSGABE ---
            st.success("Analyse abgeschlossen!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="X-Achse (Kultur & Werte)", value=f"{x_orientierung} / 10", help="0 = Traditionell | 10 = Postmodern")
            with col2:
                st.metric(label="Y-Achse (Soziale Lage)", value=f"{y_lage} / 10", help="0 = Prekär | 10 = Gehoben")
            
            st.markdown("---")
            kultur_label = "Postmodern / Progressiv" if x_orientierung >= 5 else "Traditionell / Bewahrend"
            lage_label = "Gehoben / Etabliert" if y_lage >= 5 else "Prekär / Mitte"
            
            st.info(f"**Dein berechneter Quadrant:** {lage_label} trifft auf {kultur_label}")
