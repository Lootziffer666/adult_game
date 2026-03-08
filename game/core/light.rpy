init -10 python:
    def phase_tint():
        p = ws().phase
        # leichte Tints, nicht zu bunt
        if p == "morning": return "#eef3ff"
        if p == "afternoon": return "#ffffff"
        if p == "evening": return "#ffe7c9"
        return "#cfd8ff"  # night
    
    def apply_light(location_id):
        renpy.store._current_location_for_light = location_id

screen overlay_light():
    zorder 1000
    add Solid(phase_tint()) alpha 0.08
    
    # optional: leichte Vignette nachts
    if world.phase == "night":
        add Solid("#000") alpha 0.10
