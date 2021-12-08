import random

from sbbbattlesim.action import Buff
from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = '''Toil and Trouble'''
    _level = 4

    def cast(self, player, *args, **kwargs):
        valid_targets = player.valid_characters()
        if len(valid_targets):
            targets = random.sample(valid_targets, min(len(valid_targets), 2))
            Buff(reason=StatChangeCause.TOIL_AND_TROUBLE, source=self, targets=targets,
                 health=2, attack=2, temp=False,  *args, **kwargs).resolve()
