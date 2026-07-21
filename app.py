import streamlit as st
import streamlit.components.v1 as components

# Streamlit Layout konfigurieren
st.set_page_config(
    page_title="Proximity Resonance Map",
    page_icon="🌐",
    layout="centered"
)

st.title("Proximity Resonance Map")
st.markdown("### Der soziologische Spiegel deines Begehrens")
st.write("Wähle drei prägende Beziehungs-Archetypen aus. Die Map berechnet sofort, welche Prominenten und fiktiven Ikonen dir strukturell am nächsten stehen.")

# Das vollständige 50er-Hybrid-Dataset im Backend
archetypes = {
    "Clooney": {"K1": 1, "K2": 1, "name": "George & Amal Clooney"},
    "Mulder_Scully": {"K1": 1, "K2": 1, "name": "Mulder & Scully"},
    "Curie": {"K1": 1, "K2": 1, "name": "Marie & Pierre Curie"},
    "Shrek_Fiona": {"K1": 1, "K2": 1, "name": "Shrek & Fiona"},
    "Obama": {"K1": 1, "K2": 2, "name": "Barack & Michelle Obama"},
    "Knope_Wyatt": {"K1": 1, "K2": 2, "name": "Leslie & Ben"},
    "Reynolds_Lively": {"K1": 1, "K2": 2, "name": "Ryan Reynolds & Blake Lively"},
    "Beauvoir_Sartre": {"K1": 1, "K2": 3, "name": "Simone de Beauvoir & Jean-Paul Sartre"},
    "Neo_Trinity": {"K1": 1, "K2": 3, "name": "Neo & Trinity"},
    "Russell_Hawn": {"K1": 1, "K2": 3, "name": "Kurt Russell & Goldie Hawn"},
    "Marshall_Lily": {"K1": 1, "K2": 4, "name": "Marshall & Lily"},
    "Bell_Shepard": {"K1": 1, "K2": 4, "name": "Kristen Bell & Dax Shepard"},
    "Hanks_Wilson": {"K1": 1, "K2": 4, "name": "Tom Hanks & Rita Wilson"},
    
    "Trump": {"K1": 2, "K2": 1, "name": "Donald & Melania Trump"},
    "Draper": {"K1": 2, "K2": 1, "name": "Don & Betty Draper"},
    "Charles_Diana": {"K1": 2, "K2": 1, "name": "Prinz Charles & Prinzessin Diana"},
    "Buchanan": {"K1": 2, "K2": 2, "name": "Tom & Daisy Buchanan"},
    "West_Censori": {"K1": 2, "K2": 2, "name": "Kanye West & Bianca Censori"},
    "Presley": {"K1": 2, "K2": 2, "name": "Elvis & Priscilla Presley"},
    "Joker_Harley": {"K1": 2, "K2": 3, "name": "Joker & Harley Quinn"},
    "Hefner_Madison": {"K1": 2, "K2": 3, "name": "Hugh Hefner & Holly Madison"},
    "Walter_Skyler": {"K1": 2, "K2": 3, "name": "Walter & Skyler White"},
    "Homer_Marge": {"K1": 2, "K2": 4, "name": "Homer & Marge Simpson"},
    "Klum_Kaulitz": {"K1": 2, "K2": 4, "name": "Heidi Klum & Tom Kaulitz"},
    "Jenner_Gamble": {"K1": 2, "K2": 4, "name": "Kris Jenner & Corey Gamble"},

    "Addams": {"K1": 3, "K2": 1, "name": "Gomez & Morticia Addams"},
    "Sussex": {"K1": 3, "K2": 1, "name": "Prinz Harry & Meghan Markle"},
    "Edward_Bella": {"K1": 3, "K2": 1, "name": "Edward & Bella"},
    "Fox_MGK": {"K1": 3, "K2": 2, "name": "Megan Fox & Machine Gun Kelly"},
    "Katniss_Peeta": {"K1": 3, "K2": 2, "name": "Katniss & Peeta"},
    "Beckham": {"K1": 3, "K2": 2, "name": "David & Victoria Beckham"},
    "Romeo_Julia": {"K1": 3, "K2": 3, "name": "Romeo & Julia"},
    "Cobain_Love": {"K1": 3, "K2": 3, "name": "Kurt Cobain & Courtney Love"},
    "Bonnie_Clyde": {"K1": 3, "K2": 3, "name": "Bonnie & Clyde"},
    "Ross_Rachel": {"K1": 3, "K2": 4, "name": "Ross & Rachel"},
    "Smith_Pinkett": {"K1": 3, "K2": 4, "name": "Will Smith & Jada Pinkett Smith"},
    "Bieber": {"K1": 3, "K2": 4, "name": "Justin & Hailey Bieber"},

    "Carter_Knowles": {"K1": 4, "K2": 1, "name": "Jay-Z & Beyoncé"},
    "Smith_Smith": {"K1": 4, "K2": 1, "name": "Mr. & Mrs. Smith"},
    "Batman_Catwoman": {"K1": 4, "K2": 1, "name": "Batman & Catwoman"},
    "Brady_Bundchen": {"K1": 4, "K2": 2, "name": "Tom Brady & Gisele Bündchen"},
    "Stark_Potts": {"K1": 4, "K2": 2, "name": "Tony Stark & Pepper Potts"},
    "Gates": {"K1": 4, "K2": 2, "name": "Bill & Melinda Gates"},
    "Durden_Singer": {"K1": 4, "K2": 3, "name": "Tyler Durden & Marla Singer"},
    "Burton_Carter": {"K1": 4, "K2": 3, "name": "Tim Burton & Helena Bonham Carter"},
    "Han_Leia": {"K1": 4, "K2": 3, "name": "Han Solo & Leia"},
    "Paltrow_Martin": {"K1": 4, "K2": 4, "name": "Gwyneth Paltrow & Chris Martin"},
    "Samantha_Smith": {"K1": 4, "K2": 4, "name": "Samantha & Smith"},
    "Swift_Kelce": {"K1": 4, "K2": 4, "name": "Taylor Swift & Travis Kelce"},
    "Kunis_Kutcher": {"K1": 4, "K2": 4, "name": "Mila Kunis & Ashton Kutcher"}
}

# UI Dropdowns in Streamlit
col1, col2, col3 = st.columns(3)
keys = list(archetypes.keys())

with col1:
    sel1_key = st.selectbox("Eichpunkt 1", keys, index=0, format_func=lambda x: archetypes[x]["name"])
with col2:
    sel2_key = st.selectbox("Eichpunkt 2", keys, index=5, format_func=lambda x: archetypes[x]["name"])
with col3:
    sel3_key = st.selectbox("Eichpunkt 3", keys, index=10, format_func=lambda x: archetypes[x]["name"])

# Werte für Javascript übergeben
sel1 = archetypes[sel1_key]
sel2 = archetypes[sel2_key]
sel3 = archetypes[sel3_key]

target_k1 = (sel1["K1"] + sel2["K1"] + sel3["K1"]) / 3
target_k2 = (sel1["K2"] + sel2["K2"] + sel3["K2"]) / 3

# Übergabe des Datensatzes und der Nutzer-Ziele an die D3.js Visualisierung
import json
archetypes_json = json.dumps(archetypes)

html_code = f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: transparent;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            color: #3c4043;
        }}
        #map-container {{
            position: relative;
            width: 600px;
            height: 400px;
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }}
        .tooltip {{
            position: absolute;
            text-align: center;
            padding: 8px 12px;
            font-size: 12px;
            background: #202124;
            color: #fff;
            border-radius: 6px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
            transform: translate(-50%, -100%);
            margin-top: -10px;
            z-index: 10;
            white-space: nowrap;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 60px;
            margin-top: 15px;
            font-size: 14px;
        }}
    </style>
</head>
<body>

    <div>
        <div id="map-container">
            <div id="tooltip" class="tooltip"></div>
        </div>
        <div class="stats">
            <div><strong>Feld-Dichte:</strong> <span id="density-val">High</span></div>
            <div><strong>Topologische Ausrichtung:</strong> <span id="match-val">0.00%</span></div>
        </div>
    </div>

    <script>
        const archetypes = {archetypes_json};
        const targetK1 = {target_k1};
        const targetK2 = {target_k2};

        const width = 600;
        const height = 400;
        
        const svg = d3.select("#map-container")
                      .append("svg")
                      .attr("width", width)
                      .attr("height", height);

        const tooltip = d3.select("#tooltip");

        const rings = [60, 120, 180];
        svg.selectAll(".ring")
           .data(rings)
           .enter().append("circle")
           .attr("cx", width / 2)
           .attr("cy", height / 2)
           .attr("r", d => d)
           .style("fill", "none")
           .style("stroke", "#e8eaed")
           .style("stroke-dasharray", "4,4");

        const keys = Object.keys(archetypes);
        let nodes = keys.map((key) => {
            const item = archetypes[key];
            return {
                key: key,
                name: item.name,
                K1: item.K1,
                K2: item.K2,
                r: 5,
                color: '#1a73e8',
                match: 50
            };
        });

        nodes.push({ 
            key: 'you', 
            name: 'YOU', 
            r: 16, 
            color: '#d93025', 
            fx: width / 2, 
            fy: height / 2, 
            match: 100 
        });

        const getDistance = (match) => 15 + ((100 - match) / 100) * 170;

        const simulation = d3.forceSimulation(nodes.filter(n => n.key !== 'you'))
            .force("collide", d3.forceCollide().radius(d => d.r + 4).iterations(2))
            .force("radial", d3.forceRadial(d => getDistance(d.match), width / 2, height / 2).strength(0.3))
            .on("tick", ticked);

        const nodeElements = svg.append("g")
            .selectAll("circle")
            .data(nodes)
            .enter().append("circle")
            .attr("r", d => d.r)
            .attr("fill", d => d.color)
            .style("cursor", d => d.key === 'you' ? "default" : "pointer")
            .on("mouseover", function(event, d) {
                if (d.key !== 'you') {
                    d3.select(this).attr("r", 8).attr("fill", "#1557b0");
                    tooltip.style("opacity", 1)
                           .html(`<strong>${{d.name}}</strong><br>Strukturelle Nähe: ${{d.match.toFixed(1)}}%`)
                           .style("left", (event.pageX - document.getElementById('map-container').getBoundingClientRect().left) + "px")
                           .style("top", (event.pageY - document.getElementById('map-container').getBoundingClientRect().top) + "px");
                }
            })
            .on("mouseout", function(event, d) {
                if (d.key !== 'you') {
                    d3.select(this).attr("r", d.r).attr("fill", d.color);
                    tooltip.style("opacity", 0);
                }
            });

        svg.append("text")
            .attr("x", width / 2)
            .attr("y", height / 2)
            .attr("dy", "0.3em")
            .attr("text-anchor", "middle")
            .text("YOU")
            .style("fill", "white")
            .style("font-size", "9px")
            .style("font-weight", "bold")
            .style("pointer-events", "none");

        function ticked() {
            nodeElements
                .attr("cx", d => d.key === 'you' ? width / 2 : d.x)
                .attr("cy", d => d.key === 'you' ? height / 2 : d.y);
        }

        let totalMatch = 0;
        nodes.forEach(n => {
            if (n.key !== 'you') {
                const diffK1 = Math.abs(n.K1 - targetK1);
                const diffK2 = Math.abs(n.K2 - targetK2);
                const totalDiff = Math.sqrt(diffK1 * diffK1 + diffK2 * diffK2);
                const match = Math.max(5, Math.min(98, 100 - (totalDiff / 4.24) * 90));
                n.match = match;
                totalMatch += match;
            }
        });

        const avgMatch = totalMatch / (nodes.length - 1);
        document.getElementById('match-val').innerText = avgMatch.toFixed(2) + '%';
        document.getElementById('density-val').innerText = avgMatch > 55 ? 'High' : 'Moderate';

        simulation.force("radial", d3.forceRadial(d => getDistance(d.match), width / 2, height / 2).strength(0.3));
        simulation.alpha(1).restart();
    </script>
</body>
</html>
"""

# Rendern der Komponente in Streamlit
components.html(html_code, height=480)
