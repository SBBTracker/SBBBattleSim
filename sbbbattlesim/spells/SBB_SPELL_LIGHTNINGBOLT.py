import random

from sbbbattlesim.action import Damage, ActionReason
from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = 'Lightning Bolt'
    _level = 4
    cost = 2

    def cast(self, target: 'Character' = None, *args, **kwargs):
        valid_targets = self.player.opponent.valid_characters(_lambda=lambda char: char.position in (5, 6, 7))
        if valid_targets:
            Damage(damage=10, reason=ActionReason.LIGHTNING_BOLT, source=self,
                   targets=[random.choice(valid_targets)]).resolve()
