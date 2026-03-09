init -10 python:
    from dataclasses import dataclass, field
    
    @dataclass
    class CharState:
        attention: float = 0.0
        trust: float = 0.0
        attraction: float = 0.0
        exclusivity: float = 0.0
        hard_boundary: bool = False
    
    @dataclass
    class WorldState:
        # Zeit
        day: int = 1
        minutes: int = 12*60  # Start 12:00
        phase: str = "afternoon"
        
        # Körper
        fatigue: int = 0  # 0..3
        cleanliness: int = 3  # 0..3
        
        # Public / Ort
        public_standing: float = 0.0
        dominance_image: float = 0.0
        reliability_image: float = 0.0
        rumor_heat: dict = field(default_factory=lambda: {"salon": 0.0, "home": 0.0, "bridge": 0.0})
        rumor_global: float = 0.0
        location_mood: dict = field(default_factory=lambda: {"salon": 0.0, "home": 0.0, "bridge": 0.0})
        
        # Story / Flags
        flags: set = field(default_factory=set)
        pending_story: set = field(default_factory=set)
        delayed_effects: list = field(default_factory=list)

        # Context/Hints (minimal SSOT scaffolding)
        context_tags: set = field(default_factory=set)
        memory_log: list = field(default_factory=list)
        objective_stub: str = "Observe reactions and identify patterns."
        validation_trace: list = field(default_factory=list)
        last_reaction_placeholder: str = "No new reaction recorded yet."
        
        # Exclusivity tension
        exclusivity_tension: float = 0.0
        
        # Cast
        chars: dict = field(default_factory=lambda: {
            "A": CharState(),
            "B": CharState(),
            "R": CharState(),
        })
    
    def ws():
        """Convenience accessor"""
        return renpy.store.world
