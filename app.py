import streamlit as st
from typing import Dict, Set

st.set_page_config(page_title="Iterativer KldB-Suchbaum", layout="wide")

st.title("🌲 Iterativer KldB-Suchbaum & Ausschluss-Engine")
st.markdown("Jede Eingabe verengt den Suchraum durch **progressive Elimination** unpassender KldB-Hauptbereiche und verfeinert die verbleibenden Zweige.")

# Umfassendere KldB-Struktur mit Bereichs-Profilen und Ausschluss-Logik
KLDB_TREE = {
    "Bereich 1: Land-, Forst- und Tierwirtschaft": {
        "exclude_keywords": {"landkarte", "karte", "historisch", "it", "software", "code", "forschung", "archiv"},
        "sub": ["Landwirtschaft", "Forstwirtschaft", "Tierpflege"]
    },
    "Bereich 2: Unternehmerische Führung, IT, Naturwissenschaften & Geografie": {
        "match_keywords": {"karte", "landkarte", "geografie", "daten", "analyse", "wissenschaft", "it", "forschung", "system"},
        "sub": ["Geoinformatik & Kartografie", "Wissenschaftliche Forschung", "Softwareanalyse"]
    },
    "Bereich 3: Geisteswissenschaften, Kultur, Medien & Archiv": {
        "match_keywords": {"historisch", "karte", "landkarte", "archiv", "geschichte", "kultur", "bibliothek", "museum", "sammlung"},
        "sub": ["Archiv- und Bibliothekswesen", "Museums- und Ausstellungswesen", "Historische Forschung"]
    },
    "Bereich 4: Produktion, Fertigung & Handwerk": {
        "exclude_keywords": {"landkarte", "karte", "historisch", "archiv", "forschung", "analyse"},
        "sub": ["Metallbearbeitung", "Maschinenbau", "Produktion"]
    },
    "Bereich 5: Handel, Vertrieb, Tourismus & Wachdienst": {
        "exclude_keywords": {"historisch", "archiv", "forschung", "geografie", "kartografie"},
        "sub": ["Groß- und Außenhandel", "Tourismus", "Sicherheitsdienste"]
    },
    "Bereich 6: Unternehmensbezogene Dienstleistungen, Recht & Verwaltung": {
        "match_keywords": {"verwaltung", "amt", "dokument", "ordnung", "register"},
        "sub": ["Öffentliche Verwaltung", "Vermessungs- und Katasterwesen"]
    },
    "Bereich 8: Gesundheit, Soziales, Lehre & Erziehung": {
        "exclude_keywords": {"landkarte", "karte", "historisch", "archiv", "sammlung"},
        "sub": ["Gesundheitswesen", "Sozialarbeit", "Pädagogik"]
    }
}

# Initialisierung der Historie
if "history" not in st.session_state:
    st.session_state["history"] = []

# --- 1. SEKTION: INPUT ---
st.subheader("1. Progressive Eingabe-Kette")
col_in, col_btn1, col_btn2 = st.columns([3, 1, 1])
with col_in:
    new_input = st.text_input("Geben Sie ein Merkmal ein:", placeholder="z.B. Ich sammle historische Landkarten.")
with col_btn1:
    st.write("") # Spacer
    if st.button("Hinzufügen", type="primary"):
        if new_input:
            st.session_state["history"].append(new_input.lower())
with col_btn2:
    st.write("")
    if st.button("Zurücksetzen"):
        st.session_state["history"] = []

if st.session_state["history"]:
    st.markdown("**Aktiver Suchpfad (Historie):**")
    for idx, h in enumerate(st.session_state["history"], 1):
        st.caption(f"Schritt {idx}: „{h}“")

st.divider()

# --- 2. SEKTION: BAUM-TRAVERSIERUNG & AUSSCHLUSS ---
st.subheader("2. Dynamischer Suchraum im KldB-Baum (Aktive vs. ausgeschlossene Äste)")

all_tokens = set()
for text in st.session_state["history"]:
    all_tokens.update(text.split())

active_branches = {}
excluded_branches = {}

for bereich, data in KLDB_TREE.items():
    # Prüfe, ob harte Ausschlusskriterien greifen
    excluded_by_rule = False
    if "exclude_keywords" in data:
        # Wenn spezifische Wörter vorkommen, die diesem Bereich widersprechen
        if any(kw in all_tokens for kw in data["exclude_keywords"]) and not any(pos in all_tokens for pos in data.get("match_keywords", set())):
            excluded_by_rule = True

    # Wenn noch kein Input da ist, ist alles aktiv
    if not all_tokens:
        active_branches[bereich] = data["sub"]
    elif excluded_by_rule:
        excluded_branches[bereich] = "Ausgeschlossen durch semantische Kontradiktion (Inkompatibel mit dem Input)."
    else:
        # Prüfe, ob es einen positiven Match gibt oder der Ast als neutral/relevant eingestuft wird
        has_positive = any(kw in all_tokens for kw in data.get("match_keywords", set()))
        if has_positive or not data.get("match_keywords"):
            active_branches[bereich] = data["sub"]
        else:
            # Schwache Äste werden bei fortgeschrittener Suche ausgefiltert
            if len(all_tokens) > 1:
                excluded_branches[bereich] = "Ausgefiltert (Keine positive Relevanz im Suchpfad)."
            else:
                active_branches[bereich] = data["sub"]

col_left, col_right = st.columns(2)

with col_left:
    st.markdown(f"### ✅ Verbleibender Suchraum ({len(active_branches)} Bereiche)")
    if active_branches:
        for b_name, subs in active_branches.items():
            with st.container(border=True):
                st.markdown(f"**{b_name}**")
                st.caption(relevante_subs := f"Mögliche Untergruppen: {', '.join(subs)}")
    else:
        st.warning("Keine Äste übrig. Bitte Historie anpassen.")

with col_right:
    st.markdown(f"### ❌ Systematisch ausgeschlossen ({len(excluded_branches)} Bereiche)")
    if excluded_branches:
        for b_name, reason in excluded_branches.items():
            with st.container(border=True):
                st.markdown(f"~~{b_name}~~")
                st.caption(f"Grund: {reason}")
    else:
        st.info("Bisher wurden noch keine Bereiche ausgeschlossen.")
