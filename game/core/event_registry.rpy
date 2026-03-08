init -9 python:
    def cond_public_friction(loc):
        w = ws()
        if "flag_public_friction_done" in w.flags:
            return False
        return loc == "salon"
    
    def cond_private_A(loc):
        w = ws()
        return (loc in ["home", "salon"]) and (w.chars["A"].hard_boundary is False) and (w.chars["A"].trust >= 0.7)
    
    def cond_bridge_B(loc):
        w = ws()
        return (loc == "bridge") and (w.chars["B"].attraction >= 0.6)
    
    # Register events
    register_event(EventDef(
        eid="E_PUBLIC_FRICTION",
        label="ev_public_friction",
        priority=100,
        story=True,
        cond=cond_public_friction,
        where=["salon"]
    ))
    
    register_event(EventDef(
        eid="E_PRIVATE_A",
        label="ev_private_A",
        priority=60,
        story=False,
        cond=cond_private_A,
        where=["home", "salon"]
    ))
    
    register_event(EventDef(
        eid="E_BRIDGE_B",
        label="ev_bridge_B",
        priority=60,
        story=False,
        cond=cond_bridge_B,
        where=["bridge"]
    ))
