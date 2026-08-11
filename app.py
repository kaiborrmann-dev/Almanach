import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Interaktive Topologische $\varepsilon$-Umgebung ($K_\varepsilon(x)$)")

# 1. Interaktiver Slider für Epsilon in der Sidebar
st.sidebar.header("Topologische Steuerung")
epsilon = st.sidebar.slider("Radius ε (Aktionsradius der Nachbarschaft)", min_value=0.5, max_value=8.0, value=3.0, step=0.1)

# 2. Integrierte JSON-Daten für die 15 Personen
daten = [
    {"id": "m_01", "name": "Karin", "ebene": "D4_Zentrum", "x": 0.0, "y": 0.0},
    {"id": "m_02", "name": "Anna", "ebene": "D4_Nachbarschaft", "x": 0.8, "y": 0.9},
    {"id": "m_03", "name": "Ben", "ebene": "D4_Nachbarschaft", "x": -1.5, "y": 1.5},
    {"id": "m_04", "name": "Clara", "ebene": "D4_Nachbarschaft", "x": 2.0, "y": 1.9},
    {"id": "m_05", "name": "David", "ebene": "D3_Teilstruktur", "x": 3.2, "y": 3.2},
    {"id": "m_06", "name": "Felix", "ebene": "D3_Teilstruktur", "x": -4.0, "y": -2.0},
    {"id": "m_07", "name": "Greta", "ebene": "D2_Struktur", "x": 5.1, "y": -1.0},
    {"id": "m_08", "name": "Hannes", "ebene": "D2_Struktur", "x": -5.5, "y": 2.2},
    {"id": "m_09", "name": "Ida", "ebene": "D2_Struktur", "x": 1.0, "y": -6.0},
    {"id": "m_10", "name": "Julian", "ebene": "D1_Basis", "x": -6.5, "y": -6.5},
    {"id": "m_11", "name": "Katrin", "ebene": "D1_Basis", "x": 7.0, "y": 4.0},
    {"id": "m_12", "name": "Lukas", "ebene": "D1_Basis", "x": -8.0, "y": 1.0},
    {"id": "m_13", "name": "Mia", "ebene": "D1_Basis", "x": 2.5, "y": 7.5},
    {"id": "m_14", "name": "Nils", "ebene": "D1_Basis", "x": -3.0, "y": -7.5},
    {"id": "m_15", "name": "Ole", "ebene": "D1_Basis", "x": 8.5, "y": -8.5}
]

df = pd.DataFrame(daten)

# 3. Dynamische Neuberechnung des Abstands und der Zuordnung bei jedem Slider-Move
df['d_zu_karin'] = np.sqrt(df['x']**2 + df['y']**2)

# Zuweisung basierend auf dem aktuellen Epsilon-Wert
def klassifiziere(row):
    if row['d_zu_karin'] == 0:
        return "Zentrum P(aa)"
    elif row['d_zu_karin'] < epsilon:
        return "Innerhalb K_ε (Zugetan)"
    else:
        return "Außerhalb K_ε (Distanziert)"

df['status'] = df.apply(klassifiziere, axis=1)

# 4. Datentabelle anzeigen
st.subheader(f"Strukturelle Analyse (Aktuelles ε = {epsilon})")
st.dataframe(df[['name', 'ebene', 'd_zu_karin', 'status']])

# 5. Plotly Raumansicht mit dynamischem ε-Kreis
st.subheader("Topologische Raumansicht")

fig = px.scatter(
    df, x='x', y='y', color='status', text='name',
    range_x=[-10, 10], range_y=[-10, 10],
    title=f"Dynamische ε-Umgebung (Radius = {epsilon})"
)

# Den Kreis interaktiv an den Epsilon-Wert anpassen
fig.add_shape(
    type="circle",
    xref="x", yref="y",
    x0=-epsilon, y0=-epsilon, x1=epsilon, y1=epsilon,
    line_color="rgba(0, 100, 255, 0.7)",
    fillcolor="rgba(0, 100, 255, 0.15)"
)

fig.update_traces(textposition='top center', marker=dict(size=14))
fig.update_layout(width=750, height=750)

st.plotly_chart(fig)
