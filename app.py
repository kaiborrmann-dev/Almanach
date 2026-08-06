import streamlit as st
import re

st.set_page_config(page_title="Iterativer KldB-Suchbaum", layout="wide")

st.title("🌲 Iterativer KldB-Suchbaum & Ausschluss-Engine")
st.markdown("Das System reagiert nun direkt auf jede Eingabe. Die Eingabezeile wird nach jedem Schritt automatisch geleert, und das semantische Netz scannt präzise nach inhaltlicher Relevanz.")

# --- Umfassendere KldB-Struktur mit vollständigen Keywords ---
KLDB_TREE = {
    "Bereich 1: Land-, Forst- und Tierwirtschaft": {
        "exclude_keywords": {"it", "software", "büro", "programmieren", "code", "theorie"},
        "match_keywords": {"tier", "tiere", "tierlieb", "natur", "garten", "pflanzen", "wald", "draußen", "landwirtschaft"},
        "sub": ["Landwirtschaft", "Forstwirtschaft", "Tierpflege"]
    },
    "Bereich 2: IT, Naturwissenschaften & Geografie": {
        "exclude_keywords": {"pflege", "sozial", "handwerk", "tiere"},
        "match_keywords": {"it", "computer", "daten", "software", "analyse", "wissenschaft", "logik", "karte", "landkarte"},
        "sub": ["Informatik", "Wissenschaftliche Forschung", "Geoinformatik"]
    },
    "Bereich 3: Kultur, Medien & Archiv": {
        "exclude_keywords": {"handwerk", "produktion", "pflege"},
        "match_keywords": {"historisch", "kultur", "medien", "archiv", "geschichte", "kunst", "schreiben", "lesen", "fotografie"},
        "sub": ["Archivwesen", "Medien", "Historische Forschung"]
    },
    "Bereich 4: Produktion, Fertigung & Handwerk": {
        "exclude_keywords": {"büro", "pflege", "theorie"},
        "match_keywords": {"handwerk", "produktion", "metall", "maschine", "bauen", "fertigung", "werkzeug", "reparieren"},
        "sub": ["Metallbearbeitung", "Maschinenbau", "Bauwesen"]
    },
    "Bereich 5: Handel, Vertrieb, Tourismus": {
        "exclude_keywords": {"produktion", "handwerk", "wissenschaft"},
        "match_keywords": {"handel", "verkaufen", "verkauf", "tourismus", "reise", "reisen", "urlaub", "kunden", "hotel", "gastronomie", "unterwegs"},
        "sub": ["Handel", "Tourismus", "Sicherheitsdienste"]
    },
    "Bereich 6: Recht & Verwaltung": {
        "exclude_keywords": {"handwerk", "produktion", "kreativ"},
        "match_keywords": {"verwaltung", "amt", "ordnung", "recht", "büro", "organisieren", "dokument"},
        "sub": ["Öffentliche Verwaltung", "Katasterwesen", "Recht"]
    },
    "Bereich 8: Gesundheit, Soziales, Lehre": {
        "exclude_keywords": {"maschine", "programmieren", "daten", "handel"},
        "match_keywords": {"gesundheit", "krank", "kranken", "kranke", "alt", "alten", "alte", "pflege", "pflegen", "sozial", "helfen", "menschen", "kinder", "medizin", "erziehung"},
        "sub": ["Gesundheitswesen", "Sozialarbeit", "Pädagogik"]
    }
}

# --- Session State initialisieren ---
if "history" not in st.session_state:
    st.session_state.history = []
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Callback-Funktion: Sichert Eingabe und LEERT das Textfeld sofort
def process_input():
    text = st.session_state.input_text.strip()
    if text:
        st.session_state.history.append(text)
        st.session_state.input_text = "" 

# --- 1. SEKTION: INPUT ---
st.subheader("1. Progressive Eingabe-Kette")

col_in, col_btn1, col_btn2 = st.columns([3, 1, 1])
with col_in:
    # on_change triggert den Callback automatisch, wenn "Enter" gedrückt wird
    st.text_input("Geben Sie ein Merkmal ein (z.B. 'Ich bin tierlieb' oder 'Ich reise gerne'):", 
                  key="input_text", 
                  on_change=process_input)
with col_btn1:
    st.write("") # Spacer für vertikale Ausrichtung
    st.button("Hinzufügen", type="primary", on_click=process_input)
with col_btn2:
    st.write("")
    if st.button("Zurücksetzen"):
        st.session_state.history = []
        st.session_state.input_text = ""

if st.session_state.history:
    st.markdown("**Aktiver Suchpfad (Historie):**")
    for idx, h in enumerate(st.session_state.history, 1):
        st.caption(f"Schritt {idx}: „{h}“")

st.divider()

# --- 2. SEKTION: BAUM-TRAVERSIERUNG & AUSSCHLUSS ---
st.subheader("2. Dynamischer Suchraum im KldB-Baum")

# Alle bisherigen Eingaben zusammenführen und sauber tokenisieren (Satzzeichen entfernen)
text_corpus = " ".join(st.session_state.history).lower()
all_tokens = set(re.findall(r'\b\w+\b', text_corpus))

active_branches = {}
excluded_branches = {}

# SCHRITT A: Relevanz-Scoring für alle Bereiche
branch_scores = {}
max_score = 0
for bereich, data in KLDB_TREE.items():
    score = sum(1 for kw in data["match_keywords"] if kw in all_tokens)
    branch_scores[bereich] = score
    if score > max_score:
        max_score = score

# SCHRITT B: Einordnen in Aktiv oder Ausgeschlossen
for bereich, data in KLDB_TREE.items():
    # 1. Harter Ausschluss hat absolute Priorität
    if any(kw in all_tokens for kw in data["exclude_keywords"]):
        excluded_branches[bereich] = "Ausschluss: Semantischer Widerspruch (negatives Keyword erkannt)."
        continue
    
    # 2. Wenn noch gar nichts eingegeben wurde, ist alles aktiv
    if not all_tokens:
        active_branches[bereich] = data["sub"]
        continue
        
    # 3. Logische Filterung anhand des Scores
    if max_score > 0:
        # Es gibt mindestens einen positiven Treffer im Baum
        if branch_scores[bereich] > 0:
            active_branches[bereich] = data["sub"]
        else:
            # Bereiche mit Score 0 fliegen raus, wenn andere Bereiche besser passen!
            excluded_branches[bereich] = "Ausgefiltert: Andere Branchen passen inhaltlich deutlich besser zu Ihren Eingaben."
    else:
        # Wenn nur Worte wie "ich trinke alkohol" eingegeben wurden (Score überall = 0)
        # -> Dann wird nichts willkürlich ausgeschlossen.
        active_branches[bereich] = data["sub"]

col_left, col_right = st.columns(2)

with col_left:
    st.markdown(f"### ✅ Verbleibender Suchraum ({len(active_branches)} Bereiche)")
    if active_branches:
        for b_name, subs in active_branches.items():
            with st.container(border=True):
                st.markdown(f"**{b_name}**")
                st.caption(f"Mögliche Untergruppen: {', '.join(subs)}")
    else:
        st.warning("Keine Äste übrig. Die Kombination Ihrer Aussagen schließt sich nach KldB-Logik aus.")

with col_right:
    st.markdown(f"### ❌ Ausgeschlossen ({len(excluded_branches)} Bereiche)")
    if excluded_branches:
        for b_name, reason in excluded_branches.items():
            with st.container(border=True):
                st.markdown(f"~~{b_name}~~")
                st.caption(f"Grund: {reason}")
    else:
        st.info("Bisher wurden noch keine Bereiche ausgeschlossen.")
