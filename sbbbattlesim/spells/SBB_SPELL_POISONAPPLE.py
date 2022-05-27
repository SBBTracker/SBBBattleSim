import random

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = 'Poison Apple'
    _level = 5
    cost = 2

    priority = 20

    def cast(self, target: 'Character' = None, *args, **kwargs):
        valid_targets = self.player.opponent.valid_characters()
        if valid_targets:
            target = random.choice(valid_targets)
            Buff(reason=ActionReason.POISON_APPLE, source=self, targets=[target],
                 health=-(target._base_health - 1), temp=False, *args, **kwargs).resolve()
