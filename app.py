import streamlit as st
import re

st.set_page_config(page_title="Topologische KldB-Präzisierung", layout="wide")

st.title("🎯 Topologischer KldB-Präzisions-Raum")
st.markdown("Jeder neue Input akkumuliert sich im Phasenraum. Die App berechnet fortwährend Ihre Koordinaten und zoomt von der **Makro-Ebene (Bereiche)** iterativ auf die exakte **Mikro-Ebene (5-stellige KldB-Gattung)** ein.")

# Hierarchischer, multidimensionaler Vektor-Raum der KldB
TOPOLOGICAL_KLDB_TREE = {
    "Bereich 2: IT, Software & Geoinformatik": {
        "features": {"it", "software", "daten", "code", "logik", "analyse", "algorithmus", "rechner", "programmieren", "system", "ki", "forschung", "geografie", "karte"},
        "subgroups": {
            "Hauptgruppe 24: Informatik & Software": {
                "features": {"software", "code", "programmieren", "ki", "python", "algorithmus", "entwicklung", "daten"},
                "gattungen": {
                    "24104": {"titel": "Softwareentwicklung & KI-Programmierung", "niveau": "Experte (Niveau 4)"},
                    "24102": {"titel": "IT-Systemanalyse & Datenbanken", "niveau": "Experte (Niveau 4)"}
                }
            },
            "Hauptgruppe 25: Naturwissenschaften & Forschung": {
                "features": {"forschung", "theorie", "wissenschaft", "analyse", "struktur", "akademisch", "logik"},
                "gattungen": {
                    "25192": {"titel": "Wissenschaftliche Forschung und Lehre", "niveau": "Experte / Promotion (Niveau 4)"}
                }
            }
        }
    },
    "Bereich 3: Geisteswissenschaften, Kultur & Archiv": {
        "features": {"historisch", "geschichte", "archiv", "kultur", "bibliothek", "text", "lesen", "schreiben", "quellen", "sammlung", "karte", "landkarte"},
        "subgroups": {
            "Hauptgruppe 34: Archiv, Bibliothek & Museum": {
                "features": {"archiv", "bibliothek", "sammlung", "historisch", "quellen", "karte", "geschichte", "landkarte"},
                "gattungen": {
                    "34302": {"titel": "Archivwesen und historische Dokumentation", "niveau": "Experte (Niveau 4)"}
                }
            }
        }
    },
    "Bereich 7: Landwirtschaft, Natur & Vermessung": {
        "features": {"natur", "tier", "tiere", "garten", "pflanzen", "erde", "grün", "wald", "umwelt", "geografie", "karte", "landkarte", "vermessung"},
        "subgroups": {
            "Hauptgruppe 71: Geoinformatik & Kartografie": {
                "features": {"karte", "landkarte", "geografie", "vermessung", "kartografie", "spatial", "raum"},
                "gattungen": {
                    "71392": {"titel": "Kartografie und Geoinformationswesen", "niveau": "Spezialist / Experte (Niveau 3-4)"}
                }
            }
        }
    }
}

# Session State für die kumulative Historie
if "history" not in st.session_state:
    st.session_state.history = []
if "input_box" not in st.session_state:
    st.session_state.input_box = ""

def add_input():
    text = st.session_state.input_box.strip()
    if text:
        st.session_state.history.append(text)
        st.session_state.input_box = ""

# --- 1. SEKTION: KUMULATIVER INPUT ---
st.subheader("1. Kumulativer Phasenraum des Bewerbers")
col1, col2 = st.columns([3, 1])
with col1:
    st.text_input("Geben Sie Facetten, Vorlieben oder Aussagen nacheinander ein:", 
                  key="input_box", 
                  on_change=add_input, 
                  placeholder="z.B. Ich sammle historische Landkarten...")
with col2:
    st.write("")
    if st.button("Phasenraum zurücksetzen"):
        st.session_state.history = []
        st.session_state.input_box = ""

if st.session_state.history:
    st.markdown("**Akkumulierter Vektor (Historie der Aussagen):**")
    for i, h in enumerate(st.session_state.history, 1):
        st.caption(f"Eingabe [{i}]: „{h}“")

st.divider()

# --- 2. SEKTION: TOPOLOGISCHE PRÄZISIERUNG (ZOOM-IN) ---
st.subheader("2. Topologische Präzisierung (Konvergenz im KldB-Raum)")

# Gesamten Korpus aus allen bisherigen Eingaben zusammenführen
full_corpus = " ".join(st.session_state.history).lower()
user_tokens = set(re.findall(r'\b\w+\b', full_corpus))

if not user_tokens:
    st.info("Der Phasenraum ist leer. Fügen Sie oben Aussagen hinzu, um die topologische Gravitation und Präzisierung zu starten.")
else:
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 🔭 Makro-Ebene (Bereiche im Gravitationsfeld)")
        bereich_scores = {}
        for b_name, b_data in TOPOLOGICAL_KLDB_TREE.items():
            matches = user_tokens.intersection(b_data["features"])
            score = len(matches)
            bereich_scores[b_name] = score
            
            # Visuelle Darstellung der Nähe
            intensity = "🟢 Hohe Resonanz" if score > 0 else "⚪ Distant"
            st.markdown(f"**{b_name}** — Score: `{score}` ({intensity})")
            if matches:
                st.caption(f"Aktive Koordinaten-Treffer: {', '.join(matches)}")

    with col_right:
        st.markdown("### 🔬 Mikro-Ebene (Präzisierte 5-stellige KldB-Gattungen)")
        
        # Berechne exakte Treffer auf Gattungsebene basierend auf kumulierten Vektoren
        gattung_results = []
        for b_name, b_data in TOPOLOGICAL_KLDB_TREE.items():
            for sg_name, sg_data in b_data["subgroups"].items():
                for code, g_info in sg_data["gattungen"].items():
                    # Kombinierte Features der Untergruppe und des Bereichs
                    target_features = sg_data["features"].union(b_data["features"])
                    overlap = len(user_tokens.intersection(target_features))
                    
                    # Titel-Matching als zusätzlicher Präzisionsfaktor
                    title_words = set(re.findall(r'\b\w+\b', g_info["titel"].lower()))
                    title_match = len(user_tokens.intersection(title_words))
                    
                    total_precision = overlap + (title_match * 3)
                    
                    if total_precision > 0:
                        gattung_results.append({
                            "code": code,
                            "titel": g_info["titel"],
                            "niveau": g_info["niveau"],
                            "bereich": b_name,
                            "precision": total_precision
                        })

        # Nach Präzisionsgrad sortieren (Zoom-In)
        gattung_results.sort(key=lambda x: x["precision"], reverse=True)

        if gattung_results:
            st.markdown("Das System hat folgende **topologische Konvergenzpunkte** im KldB-Baum errechnet:")
            for res in gattung_results[:3]:
                with st.container(border=True):
                    st.markdown(f"**Präziser Punkt: KldB `{res['code']}`**")
                    st.write(f"*{res['titel']}*")
                    st.caption(f"Niveau: {res['niveau']} | {res['bereich']}")
                    st.progress(min(res['precision'] / 5.0, 1.0), text=f"Topologischer Präzisions-Faktor: {res['precision']}")
        else:
            st.warning("Die kumulierten Eingaben umkreisen bisher den Raum. Fügen Sie spezifischere Begriffe hinzu (z.B. 'Karte', 'Archiv', 'Software'), um den Punkt zu schärfen.")
