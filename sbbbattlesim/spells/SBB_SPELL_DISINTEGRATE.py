import random

from sbbbattlesim.action import Damage
from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(NonTargetedSpell):
    display_name = 'Smite'
    _level = 6

    def cast(self, player, *args, **kwargs):
        valid_targets = player.opponent.valid_characters()
        if valid_targets:
            Damage(damage=30, reason=StatChangeCause.SMITE, source=self, targets=[random.choice(valid_targets)]).resolve()
