import random

from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(NonTargetedSpell):
    display_name = 'Shrivel'
    _level = 5

    def cast(self, player, *args, **kwargs):
        valid_targets = player.opponent.valid_characters()
        if valid_targets:
            target = random.choice(valid_targets)
            target.change_stats(attack=-12, health=-12, temp=False, reason=StatChangeCause.SHRIVEL, source=self, *args, **kwargs)