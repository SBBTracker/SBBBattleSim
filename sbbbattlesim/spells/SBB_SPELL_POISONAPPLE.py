import random

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import NonTargetedSpell


class SpellType(NonTargetedSpell):
    display_name = 'Poison Apple'
    _level = 5

    def cast(self, player, *args, **kwargs):
        valid_targets = player.opponent.valid_characters()
        if valid_targets:
            target = random.choice(valid_targets)
            Buff(reason=ActionReason.POISON_APPLE, source=self, targets=[target],
                 health=-(target._base_health - 1), temp=False, *args, **kwargs).resolve()
