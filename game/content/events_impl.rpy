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
                $ set_reaction_placeholder("The reaction is warmer, but still guarded.", source="ev_public_friction")
                
                "„Funktion schlägt Spott.""
                "Figur A blickt kurz auf."
                "Sie hört auf, das Uhrwerk neu zu justieren."
            
            "Scharf kontern":
                $ world.dominance_image += 0.4
                $ world.rumor_heat["salon"] += 0.3
                $ world.chars["B"].attraction += 0.3
                $ queue_delayed_effect("ev_aftershock_rumor", where=["bridge", "home"])
                $ set_reaction_placeholder("This action changes availability later, not immediately.", source="ev_public_friction")
                
                "„Du redest viel für jemanden ohne Substanz.""
                "Der Raum wird still."
                "Figur B lächelt dünn."
            
            "Ignorieren":
                $ world.chars["A"].trust -= 0.3
                $ world.rumor_heat["salon"] += 0.2
                $ set_reaction_placeholder("The room feels less cooperative after silence.", source="ev_public_friction")
                
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
                $ set_reaction_placeholder("The character stays longer than before.", source="ev_private_A")
                
                "„Du brauchst niemanden zu überzeugen.""
                "Sie hört auf, Dinge neu auszurichten."
                "Ein leises Lächeln."
            
            "Flapsig relativieren":
                $ world.chars["A"].trust -= 0.3
                $ world.chars["A"].attention -= 0.1
                $ set_reaction_placeholder("The topic closes for now.", source="ev_private_A")
                
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
                $ set_reaction_placeholder("The interaction becomes risk-forward.", source="ev_bridge_B")
                
                "„Dann lass uns sehen, was brennt.""
                "Sie kommt näher."
                "Ihr Blick wird intensiver."
            
            "Zurückhaltend bleiben":
                $ world.chars["B"].attraction -= 0.1
                $ set_reaction_placeholder("The interaction remains cautious.", source="ev_bridge_B")
                
                "„Nicht alles muss explodieren.""
                "Sie lächelt, aber bleibt auf Abstand."
    
    return


label ev_aftershock_rumor:
    "Später fällt dir auf, wie schnell sich Blicke herumsprechen."
    $ world.public_standing = max(-2.0, world.public_standing - 0.1)
    $ world.memory_log.append("Aftershock: public tension echoed beyond the original scene.")
    $ set_reaction_placeholder("A delayed reaction is now visible in another context.", source="ev_aftershock_rumor")
    return
