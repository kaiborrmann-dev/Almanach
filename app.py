import streamlit as st
import streamlit.components.v1 as components
import json

# Streamlit Layout konfigurieren
st.set_page_config(
    page_title="Proximity Resonance Map",
    page_icon="🌐",
    layout="centered"
)

st.title("Proximity Resonance Map")
st.markdown("### Der soziologische Spiegel deines Begehrens")
st.write("Klicke direkt in der Karte nacheinander auf **3 Prominente oder fiktive Ikonen**, um deine Wunsch-Konstellation zu bilden und den Raum neu zu zentrieren.")

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

archetypes_json = json.dumps(archetypes)

# HTML-Code mit direktem interaktiven Klicken auf die D3-Knoten
html_code = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: transparent;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0;
            color: #3c4043;
        }
        #map-container {
            position: relative;
            width: 600px;
            height: 400px;
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        .tooltip {
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
        }
        .selection-panel {
            margin-top: 15px;
            font-size: 13px;
            background: #f8f9fa;
            padding: 10px 20px;
            border-radius: 8px;
            border: 1px solid #dadce0;
            width: 560px;
            text-align: center;
        }
        .selected-tag {
            display: inline-block;
            background: #e8f0fe;
            color: #1a73e8;
            padding: 3px 8px;
            border-radius: 4px;
            margin: 0 4px;
            font-weight: 500;
        }
    </style>
</head>
<body>

    <div id="map-container">
        <div id="tooltip" class="tooltip"></div>
    </div>
    
    <div class="selection-panel">
        <strong>Gewählte Eichpunkte (max. 3):</strong> <span id="selection-text">Noch keine gewählt (Klicke auf Punkte)</span>
    </div>

    <script>
        const archetypes = __ARCHETYPES_JSON__;
        let selectedKeys = [];

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
                r: 6,
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
                    tooltip.style("opacity", 1)
                           .html("<strong>" + d.name + "</strong><br>Klick zum Auswählen (Eichpunkt)")
                           .style("left", (event.pageX - document.getElementById('map-container').getBoundingClientRect().left) + "px")
                           .style("top", (event.pageY - document.getElementById('map-container').getBoundingClientRect().top) + "px");
                }
            })
            .on("mouseout", function() {
                tooltip.style("opacity", 0);
            })
            .on("click", function(event, d) {
                if (d.key === 'you') return;
                
                const index = selectedKeys.indexOf(d.key);
                if (index > -1) {
                    selectedKeys.splice(index, 1); // Abwählen, wenn schon gewählt
                } else {
                    if (selectedKeys.length >= 3) {
                        selectedKeys.shift(); // Ältesten entfernen, wenn schon 3 gewählt
                    }
                    selectedKeys.push(d.key);
                }
                updateMap();
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

        function updateMap() {
            // UI aktualisieren
            const tagContainer = document.getElementById('selection-text');
            if (selectedKeys.length === 0) {
                tagContainer.innerHTML = "Noch keine gewählt (Klicke auf Punkte)";
            } else {
                tagContainer.innerHTML = selectedKeys.map(k => '<span class="selected-tag">' + archetypes[k].name + '</span>').join('');
            }

            // Farben der Knoten anpassen (Ausgewählte werden hervorgehoben)
            nodeElements.attr("fill", d => {
                if (d.key === 'you') return '#d93025';
                return selectedKeys.includes(d.key) ? '#f9ab00' : '#1a73e8';
            }).attr("r", d => selectedKeys.includes(d.key) ? 9 : 6);

            if (selectedKeys.length === 0) return;

            // Ziel-Vektoren aus den ausgewählten Punkten berechnen
            let targetK1 = 0, targetK2 = 0;
            selectedKeys.forEach(k => {
                targetK1 += archetypes[k].K1;
                targetK2 += archetypes[k].K2;
            });
            targetK1 /= selectedKeys.length;
            targetK2 /= selectedKeys.length;

            // Physik-Simulation updaten
            nodes.forEach(n => {
                if (n.key !== 'you') {
                    const diffK1 = Math.abs(n.K1 - targetK1);
                    const diffK2 = Math.abs(n.K2 - targetK2);
                    const totalDiff = Math.sqrt(diffK1 * diffK1 + diffK2 * diffK2);
                    n.match = Math.max(5, Math.min(98, 100 - (totalDiff / 4.24) * 90));
                }
            });

            simulation.force("radial", d3.forceRadial(d => getDistance(d.match), width / 2, height / 2).strength(0.3));
            simulation.alpha(1).restart();
        }

        // Standardmäßig die ersten 3 für den Start aktivieren
        selectedKeys = ['Clooney', 'Obama', 'Addams'];
        updateMap();
    </script>
</body>
</html>
"""

html_code = html_code.replace("__ARCHETYPES_JSON__", archetypes_json)
components.html(html_code, height=520)
