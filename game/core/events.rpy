init -10 python:
    class EventDef:
        def __init__(self, eid, label, priority, story, cond, where=None):
            self.eid = eid
            self.label = label
            self.priority = priority  # higher = earlier
            self.story = story  # True => can pend
            self.cond = cond  # fn(location_id) -> bool
            self.where = where or []  # [] => anywhere
    
    EVENTS = []
    
    def register_event(ev):
        EVENTS.append(ev)
    
    def pend(eid):
        w = ws()
        w.pending_story.add(eid)
    
    def clear_pending(eid):
        ws().pending_story.discard(eid)
    
    def is_pending(eid):
        return eid in ws().pending_story
    
    def eligible_events(location_id):
        w = ws()
        elig = []
        
        # normal eligibles
        for ev in EVENTS:
            if ev.where and location_id not in ev.where:
                continue
            if ev.cond(location_id):
                elig.append(ev)
        
        # pending story should also be eligible when conditions fit
        for eid in list(w.pending_story):
            ev = next((x for x in EVENTS if x.eid == eid), None)
            if ev is None:
                continue
            if ev.where and location_id not in ev.where:
                continue
            if ev.cond(location_id):
                elig.append(ev)
        
        # highest prio first, stable
        elig.sort(key=lambda e: e.priority, reverse=True)
        return elig
    
    def trigger_best(location_id):
        elig = eligible_events(location_id)
        if not elig:
            return False
        
        ev = elig[0]
        clear_pending(ev.eid)
        renpy.call(ev.label)
        return True
    
    def update_exclusivity():
        w = ws()
        A = w.chars["A"]
        B = w.chars["B"]
        
        # Basierend auf emotionaler Nähe
        tension = 0.0
        tension += max(0.0, A.trust + A.attention - 1.2)
        tension += max(0.0, B.attraction + B.attention - 1.2)
        
        # Wenn beide aktiv
        if A.trust > 0.7 and B.attraction > 0.7:
            tension += 0.5
        
        # Dämpfen
        tension *= 0.5
        
        # Global speichern
        w.exclusivity_tension = max(0.0, min(3.0, tension))
