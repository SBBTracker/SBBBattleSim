import random

from sbbbattlesim.action import Buff
from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(NonTargetedSpell):
    display_name = 'Poison Apple'
    _level = 5

    def cast(self, player, *args, **kwargs):
        valid_targets = player.opponent.valid_characters()
        if valid_targets:
            target = random.choice(valid_targets)
            Buff(reason=StatChangeCause.POISON_APPLE, source=self, targets=[target],
                 health=-(target._base_health - 1), temp=False,  *args, **kwargs).resolve()
