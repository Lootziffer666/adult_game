init -10 python:
    def compute_phase(mins):
        m = mins % (24*60)
        if 6*60 <= m < 12*60: return "morning"
        if 12*60 <= m < 18*60: return "afternoon"
        if 18*60 <= m < 22*60: return "evening"
        return "night"
    
    def advance_time(delta):
        w = ws()
        w.minutes += delta
        while w.minutes >= 24*60:
            w.minutes -= 24*60
            w.day += 1
            nightly_tick()
        w.phase = compute_phase(w.minutes)
    
    def nightly_tick():
        w = ws()
        w.cleanliness = max(0, w.cleanliness - 1)
        for loc in w.rumor_heat:
            w.rumor_heat[loc] *= 0.85
            w.location_mood[loc] *= 0.85
    
    def sleep_to_morning():
        w = ws()
        w.minutes = 6*60
        w.phase = "morning"
        w.fatigue = 0
        w.cleanliness = 3
        w.day += 1
