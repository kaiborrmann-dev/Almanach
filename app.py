import streamlit as st
from typing import Set, Tuple, List, Dict

class Actor:
    def __init__(self, id_str: str, predicates: Set[str], operators: Dict[str, str]):
        # Axiom A1 Entsprechung: Akteure als individuelle Subjekttermini (D4)
        self.id_str = id_str
        self.predicates = predicates  # Prädikattermini
        self.operators = operators    # Vektorfelder wie mA (Modus), kA (Kontext)

class PluralPairCalculus:
    def __init__(self, actors: List[Actor]):
        self.actors = actors

    def is_plural_pair(self, x: Actor, y: Actor) -> bool:
        """
        Pluralogische Bedingung für Paar(xx):
        Exakt zwei distinkte Individuen bilden die Pluralität, ohne ein neues Mengen-Objekt zu reifizieren.
        """
        return x.id_str != y.id_str

    def wahlverwandtschaft(self, x: Actor, y: Actor) -> bool:
        """
        Operationalisierung der Wahlverwandtschaft W(x, y):
        Basiert auf Wessel Tafel 8 (Echter Durchschnitt der Prädikate: P1 ∩ P2 ≠ ∅) 
        kombiniert mit der Passung im modalen Vektorfeld (mA).
        """
        # Tafel 8: Echter Durchschnitt der Prädikatsmengen
        common_predicates = x.predicates.intersection(y.predicates)
        has_real_intersection = len(common_predicates) > 0

        # Modale Raum-Passung (Operator mA)
        modality_match = x.operators.get("mA") == y.operators.get("mA")

        return has_real_intersection and modality_match

    def compute_elective_affinity_pairs(self) -> List[Tuple[Actor, Actor]]:
        """
        Ermittelt alle validen pluralen Paare Paar(xx), die über Wahlverwandtschaft verbunden sind.
        """
        plural_pairs = []
        n = len(self.actors)
        
        for i in range(n):
            for j in range(i + 1, n):
                x = self.actors[i]
                y = self.actors[j]
                
                if self.is_plural_pair(x, y) and self.wahlverwandtschaft(x, y):
                    plural_pairs.append((x, y))
                    
        return plural_pairs


# --- STREAMLIT OBERFLÄCHE ---
st.set_page_config(page_title="Axiomatischer Kalkül: Wahlverwandtschaften", layout="centered")

st.title("⚙️ Axiomatisches Analyse-Labor: Pluralogische Paarbildung")
st.markdown("Echte Profile treffen auf den formalen Kalkül (Wessel Tafel 8 & modale Operatoren).")

if "actor_pool" not in st.session_state:
    st.session_state["actor_pool"] = []

# 1. EINGABE FORMULAR
st.subheader("1. Akteur in den Raum einspeisen")
with st.form("profile_form", clear_on_submit=True):
    name = st.text_input("Name / Alias der Person")
    preds_input = st.text_input("Prädikattermini (kommagetrennt, z.B. rot, dynamisch, rational)")
    modus = st.selectbox("Modus-Operator (mA)", ["Modus_Alpha", "Modus_Beta", "Modus_Gamma"])
    
    submitted = st.form_submit_button("Akteur registrieren")
    
    if submitted and name and preds_input:
        preds = set(p.strip().lower() for p in preds_input.split(",") if p.strip())
        ops = {"mA": modus, "kA": "Kontext_Echt"}
        
        new_actor = Actor(id_str=name, predicates=preds, operators=ops)
        st.session_state["actor_pool"].append(new_actor)
        st.success(f"Akteur '{name}' erfolgreich mit Prädikaten {preds} angelegt.")

st.divider()

# 2. BESTANDS-ANZEIGE
st.subheader("2. Aktueller Akteurs-Bestand im Raum")
pool = st.session_state["actor_pool"]

if pool:
    for a in pool:
        st.write(f"- **{a.id_str}** | Prädikate: `{list(a.predicates)}` | Modus: `{a.operators['mA']}`")
        
    st.divider()
    
    # 3. BERECHNUNG
    st.subheader("3. Kalkül-Ausführung")
    if st.button("Wahlverwandtschaften P(xx) berechnen"):
        calculus = PluralPairCalculus(pool)
        result_pairs = calculus.compute_elective_affinity_pairs()
        
        st.success(f"Erfolgreich ermittelte Wahlverwandtschafts-Paare Paar(xx): {len(result_pairs)}")
        st.markdown("-" * 40)
        
        if result_pairs:
            for idx, (a1, a2) in enumerate(result_pairs, 1):
                shared_preds = a1.predicates.intersection(a2.predicates)
                st.write(f"**Paar {idx}:** `({a1.id_str}, {a2.id_str})`")
                st.write(f"  -> Modus (mA): `{a1.operators['mA']}`")
                st.write(f"  -> Gemeinsame Prädikate (Tafel 8 Intersection): `{list(shared_preds)}`")
                st.markdown("-" * 40)
        else:
            st.warning("Keine Paare erfüllen die harten Bedingungen (Schnittmenge nach Tafel 8 UND gleicher Modus mA).")
else:
    st.info("Noch keine Akteure im Raum. Lege oben mindestens zwei Profile an.")
