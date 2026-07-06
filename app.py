# SOZIOLOGISCHE_DEMYSTIFIZIERUNGS_LOGIK (SD_Logik)

def analyze_portrait(image_data):
    # 1. Extraktion der Hexis-Parameter (Körperhaltung, Raumaneignung)
    hexis_vector = extract_hexis(image_data) #
    
    # 2. Anwendung des Ordnungsverfahrens B (Ähnlichkeit der Hexis)
    # B = c_hexis (Vergleich mit Milieu-Normen)
    norm_congruence = calculate_B(hexis_vector) #
    
    # 3. Logische Fixierung durch Operatoren (Handbuch)
    # mA (Modus), lA (Bedeutung), sA (Sachverhalt), zA (Zuweisung)
    status = apply_operators(norm_congruence) #
    
    # 4. Strukturelle Klassifikation nach D1-D4
    # D4 definiert die Inklusion D ⊂ C ⊂ A
    d4_status = verify_d4_inclusion(hexis_vector) #
    
    return {
        "mA": status.mode,
        "lA": status.meaning,
        "sA": status.referent,
        "zA": status.assignment,
        "D4_Klassifikation": d4_status,
        "Trigger": "Modul_15_Bedingung" if d4_status == "Misfit" else "Modul_14_Geprüft"
    }
