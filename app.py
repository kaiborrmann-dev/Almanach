import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Topologische $\varepsilon$-Umgebung & Hierarchie-Differenzierung")

# 1. Interaktiver Slider für Epsilon in der Sidebar
st.sidebar.header("Topologische Steuerung")
epsilon = st.sidebar.slider("Radius ε (Nachbarschafts-Aktionsradius)", min_value=0.5, max_value=8.0, value=3.0, step=0.1)

# 2. Integrierte Daten mit klarer hierarchischer Zuordnung (D1 bis D4)
daten = [
    {"id": "m_01", "name": "Karin", "ebene": "D4", "x": 0.0, "y": 0.0},
    {"id": "m_02", "name": "Anna", "ebene": "D4", "x": 0.8, "y": 0.9},
    {"id": "m_03", "name": "Ben", "ebene": "D4", "x": -1.5, "y": 1.5},
    {"id": "m_04", "name": "Clara", "ebene": "D4", "x": 2.0, "y": 1.9},
    {"id": "m_05", "name": "David", "ebene": "D3", "x": 3.2, "y": 3.2},
    {"id": "m_06", "name": "Felix", "ebene": "D3", "x": -4.0, "y": -2.0},
    {"id": "m_07", "name": "Greta", "ebene": "D2", "x": 5.1, "y": -1.0},
    {"id": "m_08", "name": "Hannes", "ebene": "D2", "x": -5.5, "y": 2.2},
    {"id": "m_09", "name": "Ida", "ebene": "D2", "x": 1.0, "y": -6.0},
    {"id": "m_10", "name": "Julian", "ebene": "D1", "x": -6.5, "y": -6.5},
    {"id": "m_11", "name": "Katrin", "ebene": "D1", "x": 7.0, "y": 4.0},
    {"id": "m_12", "name": "Lukas", "ebene": "D1", "x": -8.0, "y": 1.0},
    {"id": "m_13", "name": "Mia", "ebene": "D1", "x": 2.5, "y": 7.5},
    {"id": "m_14", "name": "Nils", "ebene": "D1", "x": -3.0, "y": -7.5},
    {"id": "m_15", "name": "Ole", "ebene": "D1", "x": 8.5, "y": -8.5}
]

df = pd.DataFrame(daten)

# 3. Abstände berechnen und prüfen, ob sie zusätzlich in K_epsilon liegen
df['d_zu_karin'] = np.sqrt(df['x']**2 + df['y']**2)
df['in_epsilon_ka'] = df['d_zu_karin'] < epsilon

# 4. Datentabelle anzeigen
st.subheader(f"Strukturelle Analyse (Aktuelles ε = {epsilon})")
st.dataframe(df[['name', 'ebene', 'd_zu_karin', 'in_epsilon_ka']])

# 5. Plotly Raumansicht: Farbliche Differenzierung exakt nach logischer Ebene (D1 bis D4)
st.subheader("Topologische Raumansicht (Farbe = Hierarchieebene D1-D4)")

fig = px.scatter(
    df, x='x', y='y', color='ebene', text='name',
    range_x=[-10, 10], range_y=[-10, 10],
    category_orders={"ebene": ["D1", "D2", "D3", "D4"]},
    title=f"Hierarchische Struktur & Dynamische ε-Umgebung (Radius = {epsilon})"
)

# Den interaktiven Epsilon-Kreis einzeichnen
fig.add_shape(
    type="circle",
    xref="x", yref="y",
    x0=-epsilon, y0=-epsilon, x1=epsilon, y1=epsilon,
    line_color="rgba(255, 0, 0, 0.6)",
    fillcolor="rgba(255, 0, 0, 0.05)"
)

fig.update_traces(textposition='top center', marker=dict(size=14))
fig.update_layout(width=750, height=750)

st.plotly_chart(fig)
