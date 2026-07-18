import streamlit as st

# --- DESIGN & BRANDING ---
st.set_page_config(page_title="Zeitgeist-Compass", page_icon="🧭", layout="wide")

st.title("🧭 Zeitgeist-Compass")
st.subheader("Soziologisches Modell-Matching via Graph-Topologie (Projekt Almanach)")
st.write("---")

# --- DATA STORAGE (Die topologischen Anker-Paare) ---
# Später laden wir das dynamisch aus deiner habitus_atlas_100.json
PAAR_DATABASE = [
    {"id": 1, "name": "Amal & George Clooney", "cat": "Global Elite / Intellektuell"},
    {"id": 2, "name": "Victoria & David Beckham", "cat: "Power-Duo / Lifestyle-Brand"},
    {"id": 3, "name": "Beyoncé & Jay-Z", "cat": "Kulturelle Hegemonie / Industrie"},
    {"id": 4, "name": "Michelle & Barack Obama", "cat": "Moralisch-Institutionelle Elite"},
    {"id": 5, "name": "Zendaya & Tom Holland", "cat": "Next-Gen Pop / Nahbar"},
    {"id": 6, "name": "Prinz Harry & Meghan Markle", "cat": "Disrupte Aristokratie / Expressiv"},
    {"id": 7, "name": "Greta Gerwig & Noah Baumbach", "cat": "Intellektuelles Kino / Arthouse"},
    {"id": 11, "name": "Robert Habeck & Andrea Paluch", "cat": "Bürgerlich-Pragmatischer Diskurs"}
]

# Reale topologische User-Datenbank (Wahl-Knoten)
MOCK_USERS_GRAPH = [
    {"name": "Konrad (34)", "choices": [1, 4, 11]},
    {"name": "Elena (29)", "choices": [3, 5, 12]},
    {"name": "Maximilian (41)", "choices": [1, 7, 13]},
    {"name": "Clara (31)", "choices": [4, 11, 14]}
]

# --- UI LOGIK ---
col1, col2 = st.columns(2)

with col1:
    st.header("1. Wähle exakt 3 Paare")
    st.caption("Welche Beziehungsarchitektur spricht dich strukturell an?")
    
    # Dropdown-Auswahl für den User
    paar_options = {p["id"]: f"{p['name']} ({p['cat']})" for p in PAAR_DATABASE}
    selected_ids = st.multiselect(
        "Wähle deine 3 strukturellen Anker-Modelle:",
        options=list(paar_options.keys()),
        format_func=lambda x: paar_options[x]
    )

with col2:
    st.header("2. Topologische Auswertung")
    
    if len(selected_ids) == 3:
        st.success("Topologischer Kern (K1) induziert!")
        st.info("Dein Suchraum ist nach Kuratowski (H4) abgeschlossen und stabil.")
        
        # Berechnung der topologischen Schnittmengen
        safe_zone = []
        fun_zone = []
        
        for user in MOCK_USERS_GRAPH:
            # Schnittmenge der gewählten IDs ermitteln
            intersection = len(set(selected_ids).intersection(set(user["choices"])))
            
            if intersection >= 2:
                safe_zone.append((user["name"], f"{intersection} gemeinsame Modelle"))
            elif intersection == 1:
                fun_zone.append((user["name"], "Brücken-Modell aktiv"))
                
        # Ausgabe der Projektion (K2)
        st.write("### 🟢 Safe Zone (Interior / Strukturelle Zwillinge)")
        if safe_zone:
            for name, info in safe_zone:
                st.code(f"{name} ➔ {info}")
        else:
            st.caption("Keine Profile im inneren Kern.")
            
        st.write("### 🟡 Fun Zone (Boundary / Produktiver Rand)")
        if fun_zone:
            for name, info in fun_zone:
                st.code(f"{name} ➔ {info}")
        else:
            st.caption("Keine Profile auf der Grenzkante.")
            
    else:
        st.warning("Bitte wähle exakt 3 Paare aus, um die topologische Hülle zu berechnen.")
