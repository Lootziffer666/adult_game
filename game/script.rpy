## Bohemian Steam Chic - Demo Prototype

default world = WorldState()
default _current_location_for_light = "salon"

label start:
    scene black
    show screen overlay_light
    
    "Bohemian Steam Chic – Demo"
    "Die Stadt liegt unter dir wie ein Uhrwerk, das nicht ganz rund läuft."
    "Schornsteine. Messingdächer. Fenster, die im Abendlicht glühen."
    
    jump map_screen
