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
st.markdown("### Das soziologische Kraftfeld")
st.write("Bestimme unten deine 3 Ausgangs-Eichpunkte, um dein initiales Profil zu setzen. Klicke danach beliebig auf Prominente im Feld, um deine Position dynamisch zu verschieben und die Sogwirkung zu erleben.")

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

# UI Dropdowns zur initialen Verortung (die 3 Eichpunkte des Users)
col1, col2, col3 = st.columns(3)
keys = list(archetypes.keys())

with col1:
    sel1_key = st.selectbox("Eichpunkt 1", keys, index=0, format_func=lambda x: archetypes[x]["name"])
with col2:
    sel2_key = st.selectbox("Eichpunkt 2", keys, index=4, format_func=lambda x: archetypes[x]["name"])
with col3:
    sel3_key = st.selectbox("Eichpunkt 3", keys, index=24, format_func=lambda x: archetypes[x]["name"])

initial_selection = [sel1_key, sel2_key, sel3_key]
archetypes_json = json.dumps(archetypes)
initial_selection_json = json.dumps(initial_selection)

# HTML/JS Kraftfeld-Visualisierung
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
            height: 450px;
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
        .profile-panel {
            margin-top: 15px;
            font-size: 13px;
            background: #f8f9fa;
            padding: 12px 20px;
            border-radius: 8px;
            border: 1px solid #dadce0;
            width: 560px;
            text-align: center;
        }
    </style>
</head>
<body>

    <div id="map-container">
        <div id="tooltip" class="tooltip"></div>
    </div>
    
    <div class="profile-panel" id="profile-text">
        <strong>Dein aktuelles Begehrensprofil:</strong> Berechne...
    </div>

    <script>
        const archetypes = __ARCHETYPES_JSON__;
        let activeSelection = __INITIAL_SELECTION__;

        const width = 600;
        const height = 450;
        
        const svg = d3.select("#map-container")
                      .append("svg")
                      .attr("width", width)
                      .attr("height", height);

        const tooltip = d3.select("#tooltip");

        const keys = Object.keys(archetypes);
        let nodes = keys.map((key) => {
            const item = archetypes[key];
            // Position im Raum anhand der K1/K2 Koordinaten aufspannen (kein fester Kern/Rand mehr)
            const posX = 80 + (item.K2 - 1) * 140 + (Math.random() * 30 - 15);
            const posY = 80 + (item.K1 - 1) * 90 + (Math.random() * 30 - 15);
            return {
                key: key,
                name: item.name,
                K1: item.K1,
                K2: item.K2,
                x: posX,
                y: posY,
                r: 6,
                color: '#1a73e8',
                match: 50
            };
        });

        // Der User-Punkt ("YOU") bewegt sich frei im Feld
        nodes.push({ 
            key: 'you', 
            name: 'YOU (Dein Profil)', 
            r: 14, 
            color: '#d93025', 
            x: width / 2, 
            y: height / 2, 
            match: 100 
        });

        const simulation = d3.forceSimulation(nodes)
            .force("collide", d3.forceCollide().radius(d => d.r + 5))
            .on("tick", ticked);

        const nodeElements = svg.append("g")
            .selectAll("circle")
            .data(nodes)
            .enter().append("circle")
            .attr("r", d => d.r)
            .attr("fill", d => d.color)
            .style("cursor", "pointer")
            .on("mouseover", function(event, d) {
                tooltip.style("opacity", 1)
                       .html("<strong>" + d.name + "</strong><br>" + (d.key === 'you' ? "Dein aktueller Standpunkt" : "Klick, um Position anzusteuern"))
                       .style("left", (event.pageX - document.getElementById('map-container').getBoundingClientRect().left) + "px")
                       .style("top", (event.pageY - document.getElementById('map-container').getBoundingClientRect().top) + "px");
            })
            .on("mouseout", function() {
                tooltip.style("opacity", 0);
            })
            .on("click", function(event, d) {
                if (d.key === 'you') return;
                
                // Wenn der User auf einen Promi am Rand klickt, fügen wir ihn zur aktiven Auswahl hinzu (max 3, FIFO)
                if (!activeSelection.includes(d.key)) {
                    activeSelection.shift();
                    activeSelection.push(d.key);
                    updateField();
                }
            });

        function ticked() {
            nodeElements
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);
        }

        function updateField() {
            // Berechne den neuen Schwerpunkt des Users basierend auf den 3 aktiven Punkten
            let sumK1 = 0, sumK2 = 0;
            activeSelection.forEach(k => {
                sumK1 += archetypes[k].K1;
                sumK2 += archetypes[k].K2;
            });
            const targetK1 = sumK1 / activeSelection.length;
            const targetK2 = sumK2 / activeSelection.length;

            // Zielkoordinaten für den "YOU"-Punkt im visuellen Feld
            const targetX = 80 + (targetK2 - 1) * 140;
            const targetY = 80 + (targetK1 - 1) * 90;

            // Verschiebe den YOU-Punkt sanft zum neuen Schwerpunkt
            const youNode = nodes.find(n => n.key === 'you');
            youNode.x = targetX;
            youNode.y = targetY;

            // Farben aktualisieren (Aktive Auswahl gelb markieren)
            nodeElements.attr("fill", d => {
                if (d.key === 'you') return '#d93025';
                return activeSelection.includes(d.key) ? '#f9ab00' : '#1a73e8';
            }).attr("r", d => {
                if (d.key === 'you') return 14;
                return activeSelection.includes(d.key) ? 9 : 6;
            });

            // Text-Diagnose aktualisieren
            const k1_desc = targetK1 < 1.7 ? "Egalitär" : targetK1 < 2.5 ? "Asymmetrisch" : targetK1 < 3.5 ? "Symbiotisch" : "Autonom";
            const k2_desc = targetK2 < 1.7 ? "Hermetisch" : targetK2 < 2.5 ? "Repräsentativ" : targetK2 < 3.5 ? "Subversiv" : "Offen";
            
            document.getElementById('profile-text').innerHTML = 
                "<strong>Aktive Anker:</strong> " + activeSelection.map(k => archetypes[k].name).join(" + ") + "<br>" +
                "<strong>Dein verschobenes Profil:</strong> Binnen-Dynamik: <em>" + k1_desc + "</em> | Außengrenze: <em>" + k2_desc + "</em>";

            simulation.alpha(0.5).restart();
        }

        // Initiales Feld berechnen
        updateField();
    </script>
</body>
</html>
"""

html_code = html_code.replace("__ARCHETYPES_JSON__", archetypes_json)
html_code = html_code.replace("__INITIAL_SELECTION__", initial_selection_json)

components.html(html_code, height=530)
