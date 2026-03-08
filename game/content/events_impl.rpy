label ev_public_friction:
    $ world.flags.add("flag_public_friction_done")
    
    "Rivalenfigur lächelt dünn."
    "„Feinmechanik ist hübsch. Aber nutzlos.""
    
    menu:
        "Wie reagierst du?":
            
            "Ruhig verteidigen":
                $ world.public_standing += 0.2
                $ world.chars["A"].trust += 0.4
                $ world.rumor_heat["salon"] = max(0.0, world.rumor_heat["salon"] - 0.1)
                
                "„Funktion schlägt Spott.""
                "Figur A blickt kurz auf."
                "Sie hört auf, das Uhrwerk neu zu justieren."
            
            "Scharf kontern":
                $ world.dominance_image += 0.4
                $ world.rumor_heat["salon"] += 0.3
                $ world.chars["B"].attraction += 0.3
                
                "„Du redest viel für jemanden ohne Substanz.""
                "Der Raum wird still."
                "Figur B lächelt dünn."
            
            "Ignorieren":
                $ world.chars["A"].trust -= 0.3
                $ world.rumor_heat["salon"] += 0.2
                
                "Du sagst nichts."
                "Figur A justiert das Uhrwerk neu."
    
    return

label ev_private_A:
    "Sie steht am Tisch, das Licht weich."
    "„Manchmal frage ich mich, ob das alles reicht.""
    
    menu:
        "Antwort":
            
            "Ehrlich stärken":
                $ world.chars["A"].trust += 0.5
                $ world.chars["A"].attention += 0.3
                
                "„Du brauchst niemanden zu überzeugen.""
                "Sie hört auf, Dinge neu auszurichten."
                "Ein leises Lächeln."
            
            "Flapsig relativieren":
                $ world.chars["A"].trust -= 0.3
                $ world.chars["A"].attention -= 0.1
                
                "„Mach dir nicht so viele Gedanken.""
                "Sie richtet zwei Werkzeuge exakt parallel."
                "Ihr Blick wird kühler."
    
    return

label ev_bridge_B:
    "Sie lehnt am Geländer."
    "Rauch zieht vorbei."
    "„Manchmal muss man etwas riskieren.""
    
    menu:
        "Reaktion":
            
            "Mitspielen":
                $ world.chars["B"].attraction += 0.4
                $ world.chars["B"].attention += 0.2
                $ world.dominance_image += 0.2
                $ world.rumor_heat["bridge"] += 0.1
                
                "„Dann lass uns sehen, was brennt.""
                "Sie kommt näher."
                "Ihr Blick wird intensiver."
            
            "Zurückhaltend bleiben":
                $ world.chars["B"].attraction -= 0.1
                
                "„Nicht alles muss explodieren.""
                "Sie lächelt, aber bleibt auf Abstand."
    
    return
