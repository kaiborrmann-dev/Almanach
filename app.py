def analysiere_hexis(image):
    # Simulation der internen Kongruenzprüfung (sA)
    # In der finalen Version erfolgt hier der Abgleich mit dem Ordnungsverfahren B
    score_congruence = 0.92  # Beispielwert für Levon3.jpg
    
    # zA-Zuweisungs-Logik:
    if score_congruence >= 0.9:
        typ = "Je ne sais quoi / Elite"
    elif score_congruence >= 0.5:
        typ = "Funktionaler Pragmatiker"
    else:
        typ = "Misfit / Diskrepant"
        
    return {
        "tA": "Bild-Datensatz",
        "lA": "Habitus-Analyse",
        "sA": f"Kongruenz-Score: {score_congruence}",
        "zA": f"Zuweisung: {typ}",
        "mA": "Analytischer Modus",
        "status": "Demystifizierung abgeschlossen"
    }
