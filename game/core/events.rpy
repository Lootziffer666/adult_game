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

    def trace_validation(message):
        w = ws()
        w.validation_trace.append(message)
        # keep a small rolling window for readability
        if len(w.validation_trace) > 40:
            w.validation_trace = w.validation_trace[-40:]

    def set_reaction_placeholder(text, source="system"):
        w = ws()
        w.last_reaction_placeholder = text
        w.memory_log.append(text)
        trace_validation(f"[{source}] {text}")


    def queue_delayed_effect(label, where=None, cond=None):
        """
        Minimal delayed consequence hook.
        label: Ren'Py label to call later.
        where: optional location whitelist.
        cond: optional callable(location_id)->bool.
        """
        trace_validation(f"queue_delayed_effect:{label} where={where or []}")
        ws().delayed_effects.append({
            "label": label,
            "where": where or [],
            "cond": cond,
        })

    def resolve_delayed_effects(location_id):
        w = ws()
        if not w.delayed_effects:
            return False

        remaining = []
        fired = False
        for eff in w.delayed_effects:
            where = eff.get("where") or []
            if where and location_id not in where:
                remaining.append(eff)
                continue

            cond = eff.get("cond")
            if callable(cond) and not cond(location_id):
                remaining.append(eff)
                continue

            trace_validation(f"resolve_delayed_effect:{eff['label']} at {location_id}")
            renpy.call(eff["label"])
            fired = True

        w.delayed_effects = remaining
        return fired

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
        # Delayed effects get first chance to materialize.
        if resolve_delayed_effects(location_id):
            return True

        elig = eligible_events(location_id)
        if not elig:
            set_reaction_placeholder("The topic does not open under current conditions.", source="no_event")
            return False

        ev = elig[0]
        trace_validation(f"trigger_best:{ev.eid} at {location_id}")
        clear_pending(ev.eid)
        renpy.call(ev.label)
        return True

    def update_world_context(location_id):
        # TODO(SSOT-yellow): confirm whether passive map-idle time should always advance.
        w = ws()
        # Keep global rumor summary live as context hook.
        if w.rumor_heat:
            w.rumor_global = sum(w.rumor_heat.values()) / float(len(w.rumor_heat))

        # Lightweight context tags for narrative flavor / hinting.
        w.context_tags.discard("high_rumor")
        if w.rumor_global >= 0.6:
            w.context_tags.add("high_rumor")

        if location_id in ["salon", "bridge", "home"]:
            w.context_tags.add("visited_" + location_id)

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
