import streamlit as st
from typing import Set, Tuple, List, Dict

st.set_page_config(page_title="Strukturlogisches Arbeitsmarkt-Matching", layout="wide")

st.title("🏛️ Strukturlogischer Arbeitsmarkt-Demonstrator")
st.markdown("**Überwindung des formalen Matchens durch soziologische Topologie und relationale Logik.**")
st.markdown("Dieser Prototyp zeigt, wie Passung im Arbeitsmarkt nicht über starre bürokratische Code-Raster erfolgt, sondern über den formalen Kalkül der *Wahlverwandtschaft* (Modus $\\text{mA}$, Kontext $\\text{kA}$, Prädikatsschnittmenge).")

class Actor:
    def __init__(self, id_str: str, role: str, predicates: Set[str], operators: Dict[str, str], description: str):
        self.id_str = id_str
        self.role = role  # "Bewerber" oder "Arbeitgeber"
        self.predicates = predicates
        self.operators = operators
        self.description = description

# Initialisierung des Arbeitsmarkt-Pools in session_state
if "market_pool" not in st.session_state:
    st.session_state["market_pool"] = [
        Actor(
            id_str="KI-Forschungsinstitut Berlin", 
            role="Arbeitgeber", 
            predicates={"ki", "analyse", "formale_logik", "forschung", "struktur", "python"}, 
            operators={"mA": "Autonom-Akademisch", "kA": "Berlin-KI-Sektor"},
            description="Sucht Querdenker für strukturierte Datenmodelle und formale Analysen."
        ),
        Actor(
            id_str="Tech-StartUp Berlin Mitte", 
            role="Arbeitgeber", 
            predicates={"ki", "software", "agil", "python", "matching", "innovation"}, 
            operators={"mA": "Agil-Innovativ", "kA": "Berlin-KI-Sektor"},
            description="Baut smarte Matching-Engines und sucht interdisziplinäre Köpfe."
        ),
        Actor(
            id_str="Dr. phil. (Geisteswissenschaften / Quereinsteiger)", 
            role="Bewerber", 
            predicates={"formale_logik", "analyse", "struktur", "forschung", "python"}, 
            operators={"mA": "Autonom-Akademisch", "kA": "Berlin-KI-Sektor"},
            description="Promovierter Akademiker mit starkem methodischen Fundament und eigenem Tech-Know-how."
        )
    ]

# 1. EINGABE IN DER SEITENLEISTE
st.sidebar.header("1. Profil in den Raum einspeisen")
user_role = st.sidebar.selectbox("Rolle im Arbeitsmarkt", ["Bewerber (Arbeitnehmer)", "Arbeitgeber (Stelle/Unternehmen)"])
name_input = st.sidebar.text_input("Name / Institution", value="Muster-Bewerber")
desc_input = st.sidebar.text_area("Beschreibung / Hintergrund", value="Fokus auf Strukturlogik, Analyse und moderne Tools.")

pred_options = ["ki", "analyse", "formale_logik", "forschung", "struktur", "python", "agil", "matching", "innovation", "projektmanagement"]
selected_preds = st.sidebar.multiselect("Prädikattermini (Fähigkeiten / Merkmale)", options=pred_options, default=["analyse", "struktur"])

modus_input = st.sidebar.selectbox("Modus-Operator (mA - Arbeitsstil/Kultur)", ["Autonom-Akademisch", "Agil-Innovativ", "Hierarchisch-Klassisch"])
kontext_input = st.sidebar.selectbox("Kontext-Operator (kA - Branchenfeld)", ["Berlin-KI-Sektor", "Öffentlicher Dienst", "Traditioneller Mittelstand"])

if st.sidebar.button("Akteur registrieren"):
    role_val = "Bewerber" if "Bewerber" in user_role else "Arbeitgeber"
    new_actor = Actor(
        id_str=name_input,
        role=role_val,
        predicates=set(selected_preds),
        operators={"mA": modus_input, "kA": kontext_input},
        description=desc_input
    )
    st.session_state["market_pool"].append(new_actor)
    st.success(f"'{name_input}' erfolgreich im System registriert!")

st.divider()

# 2. BESTANDS-ANZEIGE
st.subheader("2. Aktueller Akteurs-Bestand im Arbeitsmarkt-Raum")
pool = st.session_state["market_pool"]

for act in pool:
    with st.expander(f"[{act.role}] {act.id_str} | Modus: `{act.operators['mA']}` | Kontext: `{act.operators['kA']}`"):
        st.write(f"**Beschreibung:** {act.description}")
        st.caption(f"Prädikattermini: {list(act.predicates)}")

st.divider()

# 3. BERECHNUNG DES MATCHINGS
st.subheader("3. Strukturlogische Passungs-Analyse P(xx)")
st.markdown("Ausführung nach dem relationalen Kern: $\\text{mA}(A_1) \\sim \\text{mA}(A_2) \\land \\text{kA}(A_1) = \\text{kA}(A_2) \\land (P_1 \\cap P_2 \\neq \\emptyset) \\implies P(xx)$")

if st.button("Arbeitsmarkt-Kalkül ausführen"):
    matches = []
    n = len(pool)
    for i in range(n):
        for j in range(i + 1, n):
            x = pool[i]
            y = pool[j]
            
            # Matching greift zwischen unterschiedlichen Rollen (Bewerber <-> Arbeitgeber)
            if x.role != y.role:
                modality_match = x.operators["mA"] == y.operators["mA"]
                context_match = x.operators["kA"] == y.operators["kA"]
                common_preds = x.predicates.intersection(y.predicates)
                has_intersection = len(common_preds) > 0
                
                if modality_match and context_match and has_intersection:
                    matches.append((x, y, common_preds))

    if matches:
        st.success(f"{len(matches)} valide Passungen $P(xx)$ im Arbeitsmarkt-Raum ermittelt:")
        for idx, (a1, a2, shared) in enumerate(matches, 1):
            st.markdown(f"**Match {idx}:** `{a1.id_str}` ⟷ `{a2.id_str}`")
            st.write(f"* Übereinstimmender Modus ($\\text{mA}$): `{a1.operators['mA']}`")
            st.write(f"* Übereinstimmender Kontext ($\\text{kA}$): `{a1.operators['kA']}`")
            st.caption(f"* Inhaltliche Prädikatschnittmenge ($P_1 \\cap P_2$): {list(shared)}")
            st.markdown("---")
    else:
        st.warning("Keine validen Paare gefunden. Die Modus-Passung, der Kontext oder die Prädikate weichen voneinander ab. Stellen Sie sicher, dass Arbeitgeber und Bewerber im selben Feld (z.B. Berlin-KI-Sektor) agieren und gemeinsame Merkmale teilen.")
