label location_salon:
    $ advance_time(15)
    $ apply_light("salon")
    
    scene bg black with fade
    "Salon. Gaslicht, Messing, leises Klirren."
    "Dampf steigt aus einem kleinen Apparat an der Wand."
    
    $ triggered = trigger_best("salon")
    $ update_world_context("salon")
    $ update_exclusivity()
    
    jump map_screen

label location_home:
    $ advance_time(15)
    $ apply_light("home")
    
    scene bg black with fade
    "Dein Atelier. Dampf in den Rohren."
    "Werkzeuge liegen ordentlich auf dem Tisch."
    
    $ triggered = trigger_best("home")
    $ update_world_context("home")
    $ update_exclusivity()
    
    jump map_screen

label location_bridge:
    $ advance_time(15)
    $ apply_light("bridge")
    
    scene bg black with fade
    "Die Brücke. Rauch steigt aus den Schloten."
    "Kühler Wind. Metallgeräusche."
    
    $ triggered = trigger_best("bridge")
    $ update_world_context("bridge")
    $ update_exclusivity()
    
    jump map_screen
