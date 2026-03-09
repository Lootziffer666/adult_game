default debug_overlay_enabled = False

screen map_screen():
    tag map
    
    frame:
        xalign 0.5
        yalign 0.5
        padding (40, 40)
        
        vbox:
            spacing 20
            
            text "Tag [world.day] – [world.phase]" size 24 color "#fff"
            text "Zeit: [world.minutes // 60]:[(world.minutes % 60):02d]" size 18 color "#aaa"
            text "Lab Ziel: [world.objective_stub]" size 14 color "#9ab"
            text "Letzte Reaktion: [world.last_reaction_placeholder]" size 14 color "#bcd"
            
            null height 20
            
            textbutton "Salon" action Jump("location_salon") xsize 200
            textbutton "Atelier" action Jump("location_home") xsize 200
            textbutton "Brücke" action Jump("location_bridge") xsize 200
            
            null height 20
            
            textbutton "Schlafen" action Function(sleep_to_morning) xsize 200
            
            null height 30
            
            textbutton "Dev Debug: ['ON' if debug_overlay_enabled else 'OFF']" action ToggleVariable("debug_overlay_enabled") xsize 200

            if debug_overlay_enabled:
                frame:
                    background "#000a"
                    padding (10, 10)

                    vbox:
                        spacing 5
                        text "DEBUG" size 14 color "#f80"
                        text "A: Trust [world.chars['A'].trust:.2f] | Att [world.chars['A'].attention:.2f]" size 12
                        text "B: Attr [world.chars['B'].attraction:.2f] | Att [world.chars['B'].attention:.2f]" size 12
                        text "Exclusivity: [world.exclusivity_tension:.2f]" size 12
                        text "Rumor(salon): [world.rumor_heat['salon']:.2f] | Global: [world.rumor_global:.2f]" size 12
                        text "Fatigue: [world.fatigue] | Clean: [world.cleanliness]" size 12
                        text "Context: [', '.join(sorted(list(world.context_tags)))]" size 12
                        text "Trace tail: [world.validation_trace[-1] if world.validation_trace else '(none)']" size 12

label map_screen:
    call screen map_screen
