import streamlit as st
import streamlit.components.v1 as components
import json

# Streamlit Layout konfigurieren
st.set_page_config(
    page_title="Proximity Resonance Map",
    page_icon="🌐",
    layout="centered"
)

st.title("Der Beziehungs-Spiegel")
st.markdown("### Welche Beziehungs-Architektur suchst du wirklich?")

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

# Schritt 1: Die intuitive Eingabe im oberen Bereich
st.markdown("### 1. Welche Paare führen deiner Meinung nach eine gute Beziehung?")
st.write("Wähle drei Paare aus, die dich inspirieren:")

col1, col2, col3 = st.columns(3)
keys = list(archetypes.keys())

with col1:
    sel1_key = st.selectbox("Erstes Paar", keys, index=0, format_func=lambda x: archetypes[x]["name"])
with col2:
    sel2_key = st.selectbox("Zweites Paar", keys, index=4, format_func=lambda x: archetypes[x]["name"])
with col3:
    sel3_key = st.selectbox("Drittes Paar", keys, index=24, format_func=lambda x: archetypes[x]["name"])

initial_selection = [sel1_key, sel2_key, sel3_key]

# Backend-Berechnung des initialen Struktur-Profils
init_k1 = sum(archetypes[k]["K1"] for k in initial_selection) / 3
init_k2 = sum(archetypes[k]["K2"] for k in initial_selection) / 3
init_names = [archetypes[k]["name"] for k in initial_selection]

def generate_structural_analysis(k1, k2, names):
    # Präzise, soziologische Typen-Zuordnung ohne Geschwafel
    k1_types = {
        1: "Egalitäre Binnenstruktur (Symmetrie, Augenhöhe, Verzicht auf formale Hierarchien)",
        2: "Asymmetrische Binnenstruktur (Klares Macht- und Führungsgefälle, definierte Rollenverteilung)",
        3: "Symbiotische Binnenstruktur (Verschmelzung, Auflösung individueller Grenzen, absolute Intimität)",
        4: "Autonome Binnenstruktur (Parallele Unabhängigkeit zweier starker Akteure ohne Klammern)"
    }
    
    k2_types = {
        1: "Hermetische Außengrenze (Die uneinnehmbare Festung, absolute Abschottung nach außen)",
        2: "Repräsentative Außengrenze (Die gesellschaftliche Bühne, Inszenierung und Statuspflege)",
        3: "Subversive Außengrenze (Bruch mit bürgerlichen Konventionen, normbrechende Eigendynamik)",
        4: "Offene Außengrenze (Vollständige Durchlässigkeit und Einbindung ins soziale Netzwerk)"
    }

    rK1 = max(1, min(4, round(k1)))
    rK2 = max(1, min(4, round(k2)))
    name_str = ", ".join(names)

    return f"""
    <strong>Analytischer Befund der Anker ({name_str}):</strong><br><br>
    <strong>1. Binnen-Dimension (K1):</strong> {k1_types[rK1]}<br>
    <strong>2. Außen-Dimension (K2):</strong> {k2_types[rK2]}<br><br>
    <em>Strukturelles Fazit:</em> Deine Auswahl definiert einen exakten Schnittpunkt im Koordinatensystem. 
    Die Paare teilen eine gemeinsame Topologie, bei der interne Beziehungsmechanik und externe Grenzziehung zwingend ineinandergreifen. 
    Klickst du im Feld auf abweichende Paare, verschiebt sich dieser mathematische Schwerpunkt sofort.
    """

initial_essay = generate_structural_analysis(init_k1, init_k2, init_names)
archetypes_json = json.dumps(archetypes)
initial_selection_json = json.dumps(initial_selection)

st.markdown("---")
st.markdown("### 2. Siehst du, welche dir im Feld am nächsten sind?")
st.write("Die markierten Punkte in der Karte spiegeln deinen Schwerpunkt wider. Klicke im Feld auf andere Paare, wenn du merkst, dass sie dir eigentlich noch näher stehen – sie kalibrieren dein Profil sofort nach.")

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
            height: 420px;
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
        .explanation-panel {
            margin-top: 15px;
            margin-bottom: 30px;
            font-size: 14px;
            background: #f8f9fa;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #dadce0;
            width: 560px;
            line-height: 1.6;
        }
        .insight-title {
            font-size: 15px;
            font-weight: 600;
            color: #202124;
            margin-bottom: 10px;
            display: block;
        }
        .insight-content {
            color: #444746;
        }
    </style>
</head>
<body>

    <div id="map-container">
        <div id="tooltip" class="tooltip"></div>
    </div>
    
    <div class="explanation-panel" id="explanation-panel">
        <span class="insight-title">3. Struktureller Kern der Beziehung</span>
        <div class="insight-content" id="essay-content">__INITIAL_ESSAY__</div>
    </div>

    <script>
        const archetypes = __ARCHETYPES_JSON__;
        let activeSelection = __INITIAL_SELECTION__;

        const width = 600;
        const height = 420;
        
        const svg = d3.select("#map-container")
                      .append("svg")
                      .attr("width", width)
                      .attr("height", height);

        const tooltip = d3.select("#tooltip");

        const keys = Object.keys(archetypes);
        let nodes = keys.map((key) => {
            const item = archetypes[key];
            const posX = 70 + (item.K2 - 1) * 150 + (Math.random() * 20 - 10);
            const posY = 70 + (item.K1 - 1) * 90 + (Math.random() * 20 - 10);
            return {
                key: key,
                name: item.name,
                K1: item.K1,
                K2: item.K2,
                x: posX,
                y: posY,
                r: 6,
                color: '#1a73e8'
            };
        });

        nodes.push({ 
            key: 'you', 
            name: 'Dein Schwerpunkt', 
            r: 15, 
            color: '#d93025', 
            x: width / 2, 
            y: height / 2 
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
                       .html("<strong>" + d.name + "</strong><br>" + (d.key === 'you' ? "Dein aktueller Standort" : "Klick, um als Anker zu übernehmen"))
                       .style("left", (event.pageX - document.getElementById('map-container').getBoundingClientRect().left) + "px")
                       .style("top", (event.pageY - document.getElementById('map-container').getBoundingClientRect().top) + "px");
            })
            .on("mouseout", function() {
                tooltip.style("opacity", 0);
            })
            .on("click", function(event, d) {
                if (d.key === 'you') return;
                
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

        function generateJSAnalysis(targetK1, targetK2, names) {
            const k1_types = {
                1: "Egalitäre Binnenstruktur (Symmetrie, Augenhöhe, Verzicht auf formale Hierarchien)",
                2: "Asymmetrische Binnenstruktur (Klares Macht- und Führungsgefälle, definierte Rollenverteilung)",
                3: "Symbiotische Binnenstruktur (Verschmelzung, Auflösung individueller Grenzen, absolute Intimität)",
                4: "Autonome Binnenstruktur (Parallele Unabhängigkeit zweier starker Akteure ohne Klammern)"
            };
            
            const k2_types = {
                1: "Hermetische Außengrenze (Die uneinnehmbare Festung, absolute Abschottung nach außen)",
                2: "Repräsentative Außengrenze (Die gesellschaftliche Bühne, Inszenierung und Statuspflege)",
                3: "Subversive Außengrenze (Bruch mit bürgerlichen Konventionen, normbrechende Eigendynamik)",
                4: "Offene Außengrenze (Vollständige Durchlässigkeit und Einbindung ins soziale Netzwerk)"
            };

            const rK1 = Math.max(1, Math.min(4, Math.round(targetK1)));
            const rK2 = Math.max(1, Math.min(4, Math.round(targetK2)));
            const nameStr = names.join(', ');

            return "<strong>Analytischer Befund der Anker (" + nameStr + "):</strong><br><br>" +
                   "<strong>1. Binnen-Dimension (K1):</strong> " + k1_types[rK1] + "<br>" +
                   "<strong>2. Außen-Dimension (K2):</strong> " + k2_types[rK2] + "<br><br>" +
                   "<em>Strukturelles Fazit:</em> Deine Auswahl definiert einen exakten Schnittpunkt im Koordinatensystem. " +
                   "Die Paare teilen eine gemeinsame Topologie, bei der interne Beziehungsmechanik und externe Grenzziehung zwingend ineinandergreifen. " +
                   "Klickst du im Feld auf abweichende Paare, verschiebt sich dieser mathematische Schwerpunkt sofort.";
        }

        function updateField() {
            let sumK1 = 0, sumK2 = 0;
            activeSelection.forEach(k => {
                sumK1 += archetypes[k].K1;
                sumK2 += archetypes[k].K2;
            });
            const targetK1 = sumK1 / activeSelection.length;
            const targetK2 = sumK2 / activeSelection.length;

            const targetX = 70 + (targetK2 - 1) * 150;
            const targetY = 70 + (targetK1 - 1) * 90;

            const youNode = nodes.find(n => n.key === 'you');
            youNode.x = targetX;
            youNode.y = targetY;

            nodeElements.attr("fill", d => {
                if (d.key === 'you') return '#d93025';
                return activeSelection.includes(d.key) ? '#f9ab00' : '#1a73e8';
            }).attr("r", d => {
                if (d.key === 'you') return 15;
                return activeSelection.includes(d.key) ? 10 : 6;
            });

            const activeNames = activeSelection.map(k => archetypes[k].name);
            const analysisHtml = generateJSAnalysis(targetK1, targetK2, activeNames);

            document.getElementById('essay-content').innerHTML = analysisHtml;

            simulation.alpha(0.5).restart();
        }

        updateField();
    </script>
</body>
</html>
"""

html_code = html_code.replace("__ARCHETYPES_JSON__", archetypes_json)
html_code = html_code.replace("__INITIAL_SELECTION__", initial_selection_json)
html_code = html_code.replace("__INITIAL_ESSAY__", initial_essay)

components.html(html_code, height=750)
