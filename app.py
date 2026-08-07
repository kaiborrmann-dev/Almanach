import streamlit as st
import plotly.express as px
import pandas as pd

# Beispieldaten zur Repräsentation der KldB-Clusterstruktur
kldb_cluster_data = [
    # Abschnitt 2: Fertigungsberufe
    {"Abschnitt": "2. Fertigungsberufe", "Bereich": "25 Mechatronik & Elektro", "Gruppe": "251 Elektroberufe", "Label": "251: Elektroberufe"},
    {"Abschnitt": "2. Fertigungsberufe", "Bereich": "25 Mechatronik & Elektro", "Gruppe": "252 Mechatronik", "Label": "252: Mechatronik"},
    {"Abschnitt": "2. Fertigungsberufe", "Bereich": "26 Metallerzeugung & -bearbeitung", "Gruppe": "261 Metallbearbeitung", "Label": "261: Metallbearbeitung"},
    
    # Abschnitt 4: IT- & Naturwissenschaftliche Dienste
    {"Abschnitt": "4. IT- & Naturwissenschaft", "Bereich": "43 Informatik & IKT", "Gruppe": "431 Informatik", "Label": "431: Informatikberufe"},
    {"Abschnitt": "4. IT- & Naturwissenschaft", "Bereich": "43 Informatik & IKT", "Gruppe": "434 Softwareentwicklung", "Label": "434: Software & Programmierung"},
    {"Abschnitt": "4. IT- & Naturwissenschaft", "Bereich": "42 Technische Forschung", "Gruppe": "421 Physik & Chemie", "Label": "421: Naturwissenschaften"},
    
    # Abschnitt 5: Unternehmensbezogene Dienstleistungen
    {"Abschnitt": "5. Dienstleistungen", "Bereich": "51 Unternehmensführung", "Gruppe": "511 Unternehmensberatung", "Label": "511: Beratung & Management"},
    {"Abschnitt": "5. Dienstleistungen", "Bereich": "52 Finanzdienstleistungen", "Gruppe": "521 Banken & Versicherung", "Label": "521: Finanzwesen"}
]

df_cluster = pd.DataFrame(kldb_cluster_data)

st.markdown("### Interaktive Cluster-Landkarte des KldB-Raums")
st.markdown("Die Visualisierung zeigt die hierarchische Verschachtelung der Berufsgruppen ($N_2$) innerhalb der globalen Bereiche ($N_3$) und Abschnitte.")

# Erstellung des Sunburst-Charts zur Cluster-Darstellung
fig_cluster = px.sunburst(
    df_cluster,
    path=['Abschnitt', 'Bereich', 'Label'],
    title="Topologisches Cluster-Modell der KldB-Struktur",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig_cluster.update_layout(
    margin=dict(t=40, b=10, l=10, r=10),
    height=500
)

st.plotly_chart(fig_cluster, use_container_width=True)
