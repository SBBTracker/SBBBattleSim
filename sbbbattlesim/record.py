from dataclasses import dataclass

@dataclass
class Record:
    reason: 'ActionReason' = None
    source: ('Character', 'Hero', 'Spell', 'Treasure') = None
    target: ('Character', 'Hero', 'Spell', 'Treasure') = None
    target_id: str = None
    target_attack: int = None
    target_health: int = None
    event: 'Event' = None
    attack: int = 0
    health: int = 0
    damage: int = 0
    heal: int = 0
    quest_progress: int = 0

    def to_json(self):
        return dict(
            reason=self.reason,
            source=self.source,
            target=self.target,
            attack=self.attack,
            health=self.health,
            damage=self.damage,
            heal=self.heal,
            quest_progress=self.quest_progress,
        )