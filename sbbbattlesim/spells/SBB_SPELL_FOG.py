import random

from sbbbattlesim.action import Buff, Damage, ActionReason
from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = 'Fog'
    _level = 6
    cost = 2

    def cast(self, target: 'Character' = None, *args, **kwargs):
        valid_targets = self.player.opponent.valid_characters(_lambda=lambda char: char.ranged and char.attack > 1)
        if valid_targets:
            target = random.choice(valid_targets)
            Buff(reason=ActionReason.FOG, source=self, targets=[target],
                 attack=-(target.attack - 1), temp=False, *args, **kwargs).resolve()
