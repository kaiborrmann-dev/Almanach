import streamlit as st
from typing import Set, Tuple, List, Dict

st.set_page_config(page_title="Passgenau-Finder für Arbeit & Kultur", layout="wide")

st.title("💼 Passgenau-Finder: Arbeit, Kultur & Perspektiven")
st.markdown("Ein moderner Matching-Ansatz, der über starre Formulare hinausgeht und Menschen über geteilte Inhalte, Arbeitsstile und Kontexte passgenau zusammenbringt.")

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
            predicates={"ki", "analyse", "forschung", "struktur", "python"}, 
            operators={"mA": "Autonom & Eigenverantwortlich", "kA": "KI & Technologie"},
            description="Sucht Köpfe für strukturierte Datenmodelle, formale Analysen und zukunftsweisende Projekte."
        ),
        Actor(
            id_str="Tech-StartUp Berlin Mitte", 
            role="Arbeitgeber", 
            predicates={"ki", "software", "agil", "python", "innovation"}, 
            operators={"mA": "Agil & Interdisziplinär", "kA": "KI & Technologie"},
            description="Baut smarte Lösungen und sucht pragmatische Macher mit Begeisterung für neue Technologien."
        ),
        Actor(
            id_str="Dr. Thomas Weber (Quereinsteiger)", 
            role="Bewerber", 
            predicates={"analyse", "struktur", "forschung", "python", "methodik"}, 
            operators={"mA": "Autonom & Eigenverantwortlich", "kA": "KI & Technologie"},
            description="Geisteswissenschaftlicher Hintergrund, stark in strukturierter Analyse und eigeninitiativer Einarbeitung in Tech-Themen."
        )
    ]

# SEITENLEISTE: EINGABE
st.sidebar.header("1. Profil oder Stelle erfassen")
user_role = st.sidebar.selectbox("Ich bin...", ["Arbeitssuchende Person / Bewerber", "Arbeitgeber / Unternehmen / Stelle"])
name_input = st.sidebar.text_input("Name oder Unternehmensbezeichnung", value="Anna Schmidt")

# Intuitive Freitext-Eingabe statt starrer Kategorien
free_text_bio = st.sidebar.text_area(
    "Erzählen Sie frei über sich oder die Anforderungen (z.B. Interessen, Stärken, Visionen):",
    value="Ich interessiere mich stark für Datenanalyse, strukturierte Arbeitsweisen und KI-Technologien in Berlin."
)

st.sidebar.markdown("---")
modus_input = st.sidebar.selectbox(
    "Wie arbeiten Sie am liebsten? (Arbeitsstil / Kultur)", 
    ["Autonom & Eigenverantwortlich", "Agil & Interdisziplinär", "Strukturiert & Klassisch"]
)
kontext_input = st.sidebar.selectbox(
    "In welchem Bereich bewegen Sie sich? (Themenwelt)", 
    ["KI & Technologie", "Öffentlicher Sektor & Verwaltung", "Handel & Dienstleistung", "Kultur & Bildung"]
)

# NEBENFELD / HILFS-OPTION (Wie vom Nutzer gewünscht)
with st.sidebar.expander("📝 Lebenslauf-Assistent"):
    st.markdown("**Sollen wir Ihnen beim Erstellen eines tabellarischen Lebenslaufes behilflich sein?**")
    st.markdown("Dann benötigen wir noch folgende Angaben:")
    job_goal = st.text_input("Angestrebte Position / Ziel")
    key_skills = st.text_input("Wichtigste bisherige Stationen / Skills")
    if st.button("Daten für Lebenslauf aufbereiten"):
        st.success("Daten wurden für den Entwurf vorgemerkt!")

if st.sidebar.button("In den Vermittlungs-Raum einspeisen"):
    # Automatische Extraktion von Stichwörtern aus dem Freitext (Filter für Füllwörter)
    extracted_preds = set(w.lower().strip(".,!?;:()[]") for w in free_text_bio.split() if len(w) > 3)
    
    role_val = "Bewerber" if "Bewerber" in user_role else "Arbeitgeber"
    new_actor = Actor(
        id_str=name_input,
        role=role_val,
        predicates=extracted_preds,
        operators={"mA": modus_input, "kA": kontext_input},
        description=free_text_bio
    )
    st.session_state["market_pool"].append(new_actor)
    st.sidebar.success(f"Profil für '{name_input}' erfolgreich hinzugefügt!")

st.divider()

# 2. BESTANDS-ANZEIGE IM RAUM
st.subheader("2. Aktuelle Profile & Stellen im Vermittlungs-Pool")
pool = st.session_state["market_pool"]

cols = st.columns(2)
for idx, act in enumerate(pool):
    with cols[idx % 2]:
        with st.expander(f"[{act.role}] {act.id_str}"):
            st.write(f"**Beschreibung:** {act.description}")
            st.write(f"* **Kultur / Stil:** `{act.operators['mA']}`")
            st.write(f"* **Themenfeld:** `{act.operators['kA']}`")
            st.caption(f"Erkannte inhaltliche Resonanzpunkte: {list(act.predicates)}")

st.divider()

# 3. BERECHNUNG DER PASSUNGEN
st.subheader("3. Intelligente Passungs-Analyse (Match-Ergebnisse)")
st.markdown("Das System prüft, ob Kultur, Themenfeld und inhaltliche Interessen übereinstimmen – jenseits starrer Zeugnis-Raster.")

if st.button("Passende Verbindungen ermitteln"):
    matches = []
    n = len(pool)
    for i in range(n):
        for j in range(i + 1, n):
            x = pool[i]
            y = pool[j]
            
            # Matching zwischen unterschiedlichen Seiten (Bewerber <-> Arbeitgeber)
            if x.role != y.role:
                modality_match = x.operators["mA"] == y.operators["mA"]
                context_match = x.operators["kA"] == y.operators["kA"]
                common_preds = x.predicates.intersection(y.predicates)
                has_intersection = len(common_preds) > 0
                
                if modality_match and context_match and has_intersection:
                    matches.append((x, y, common_preds))

    if matches:
        st.success(f"Es wurden {len(matches)} passfähige Verbindungen im Raum entdeckt:")
        for idx, (a1, a2, shared) in enumerate(matches, 1):
            st.markdown(f"**Empfehlung {idx}:** `{a1.id_str}` ⟷ `{a2.id_str}`")
            st.write(f"* **Gemeinsame Arbeitskultur:** `{a1.operators['mA']}`")
            st.write(f"* **Gemeinsames Themenfeld:** `{a1.operators['kA']}`")
            st.caption(f"* Inhaltliche Schnittmengen (Themen & Interessen): {list(shared)}")
            st.markdown("---")
    else:
        st.warning("Keine exakte Passung gefunden. Versuchen Sie, in der Beschreibung ähnliche Schlüsselwörter (z.B. 'Analyse', 'Technologie') zu verwenden oder das gleiche Themenfeld zu wählen.")
