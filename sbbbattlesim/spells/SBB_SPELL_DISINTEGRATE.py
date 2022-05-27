import random

from sbbbattlesim.action import Damage, ActionReason
from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = 'Smite'
    _level = 6
    cost = 3

    def cast(self, target: 'Character' = None, *args, **kwargs):
        valid_targets = self.player.opponent.valid_characters()
        if valid_targets:
            Damage(damage=30, reason=ActionReason.SMITE, source=self, targets=[random.choice(valid_targets)]).resolve()
