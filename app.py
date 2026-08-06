import streamlit as st
from typing import Dict, List, Set

st.set_page_config(page_title="Iterativer KldB-Suchbaum", layout="wide")

st.title("🌲 Iterativer KldB-Suchbaum & Einengungs-Engine")
st.markdown("Jede neue Eingabe wirkt als logischer Operator, der den Suchraum innerhalb der hierarchischen Klassifikation der Berufe (KldB) schrittweise verengt.")

# Hierarchische KldB-Struktur (Beispiel-Baum mit Verzweigungen)
KLDB_TREE = {
    "Bereich 2: Unternehmerische Führung, IT, Naturwissenschaften": {
        "keywords": {"it", "computer", "daten", "software", "forschung", "wissenschaft", "logik", "analyse", "ki"},
        "untergruppen": {
            "241: Informatik und Software": {
                "keywords": {"software", "code", "programmieren", "ki", "python", "algorithmus", "entwicklung"},
                "gaenge": {
                    "24104": {"titel": "Softwareentwicklung & KI-Programmierung", "niveau": "Niveau 4 (Experte)"},
                    "24102": {"titel": "IT-Systemanalyse & Datenbanken", "niveau": "Niveau 4 (Experte)"}
                }
            },
            "251: Wissenschaft & Forschung": {
                "keywords": {"forschung", "theorie", "universität", "analyse", "struktur", "akademisch"},
                "gaenge": {
                    "25192": {"titel": "Wissenschaftliche Forschung und Lehre", "niveau": "Niveau 4 (Promotion)"}
                }
            }
        }
    },
    "Bereich 7: Land-, Forst-, Tierwirtschaft und Gartenbau": {
        "keywords": {"natur", "tiere", "garten", "pflanzen", "draußen", "reisen", "umwelt"},
        "untergruppen": {
            "711: Gartenbau": {
                "keywords": {"garten", "pflanzen", "erde", "grün", "landschaft"},
                "gaenge": {
                    "71102": {"titel": "Gartenbau und Landschaftsgestaltung", "niveau": "Niveau 2-3 (Fachkraft)"}
                }
            },
            "731: Tierhaltung und Pflege": {
                "keywords": {"tier", "tiere", "hund", "katze", "hof", "pflege"},
                "gaenge": {
                    "81202": {"titel": "Tierpflege und Natur-Umweltschutz", "niveau": "Niveau 2-3 (Fachkraft)"}
                }
            }
        }
    }
}

# Initialisierung der kumulativen Eingabe-Historie im Session State
if "input_history" not in st.session_state:
    st.session_state["input_history"] = []

# --- 1. SEKTION: PROGRESSIVE EINGABE-KETTE ---
st.subheader("1. Progressive Eingabe zur Baumnavigation")
user_input = st.text_input(
    "Geben Sie Merkmale, Interessen oder Aussagen ein (jeder neue Input engt den Suchbaum weiter ein):", 
    placeholder="z.B. Ich interessiere mich für IT, danach: und programmiere in Python"
)

col_btn1, col_btn2 = st.columns([1, 4])
with col_btn1:
    if st.button("Input hinzufügen", type="primary"):
        if user_input:
            st.session_state["input_history"].append(user_input.lower())
with col_btn2:
    if st.button("Suchbaum zurücksetzen"):
        st.session_state["input_history"] = []

# Historie der Einengungen anzeigen
if st.session_state["input_history"]:
    st.markdown("**Aktive Filter-Kette (Kumulativer Suchpfad):**")
    for idx, text in enumerate(st.session_state["input_history"], 1):
        st.caption(f"Schritt {idx}: „{text}“")

st.divider()

# --- 2. SEKTION: BAUM-TRAVERSIERUNG & FILTRIERUNG ---
st.subheader("2. Verbleibender Suchraum im KldB-Baum")

# Aggregierte Tokens aus der gesamten Historie bilden den Filter
all_tokens = set()
for text in st.session_state["input_history"]:
    all_tokens.update(text.split())

matching_results = []

if not all_tokens:
    st.info("Der Suchbaum ist vollständig geöffnet. Fügen Sie oben Begriffe hinzu, um den Baum von oben nach unten zu durchwandern und einzuengen.")
else:
    # Durchsuche den hierarchischen Baum anhand der kumulativen Tokens
    for bereich_name, bereich_data in KLDB_TREE.items():
        # Prüfe Bereichs-Match
        bereich_match = any(kw in all_tokens for kw in bereich_data["keywords"])
        
        for unter_name, unter_data in bereich_data["untergruppen"].items():
            # Prüfe Untergruppen-Match oder starkes Bereichssignal
            unter_match = any(kw in all_tokens for kw in unter_data["keywords"]) or bereich_match
            
            for code, details in unter_data["gaenge"].items():
                title_tokens = set(details["titel"].lower().split())
                token_overlap = len(all_tokens.intersection(title_tokens))
                
                # Wenn der Suchpfad passt, bleibt der Knoten im Suchraum
                if unter_match or token_overlap > 0:
                    matching_results.append({
                        "code": code,
                        "titel": details["titel"],
                        "niveau": details["niveau"],
                        "bereich": bereich_name,
                        "untergruppe": unter_name
                    })

    if matching_results:
        st.success(f"Suchraum erfolgreich eingeengt: **{len(matching_results)}** KldB-Berufsgattungen verbleiben im aktiven Zweig:")
        for r in matching_results:
            with st.container(border=True):
                st.markdown(f"**KldB-Code: `{r['code']}` — {r['titel']}**")
                st.write(f"* **Bereich (1. Stelle):** {r['bereich']}")
                st.write(f"* **Untergruppe:** {r['untergruppe']}")
                st.write(f"* **Anforderungsniveau (5. Stelle):** {r['niveau']}")
    else:
        st.warning("Die kumulierten Eingaben haben den Suchbaum vollständig isoliert (Keine Verzweigung im KldB-Baum passt zu dieser Kombination). Setzen Sie den Baum zurück oder passen Sie die Eingabe an.")
