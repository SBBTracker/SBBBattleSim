from dataclasses import dataclass

@dataclass
class Record:
    reason: ('ActionReason', None) = None
    source: ('Character', 'Hero', 'Spell', 'Treasure', None) = None
    target: ('Character', 'Hero', 'Spell', 'Treasure', None) = None
    event: ('Event', None) = None
    attack: int = 0
    health: int = 0
    damage: int = 0
    heal: int = 0

    def to_json(self):
        return dict(
            reason=self.reason,
            source=self.source,
            target=self.target,
            attack=self.attack,
            health=self.health,
            damage=self.damage,
            heal=self.heal,
        )