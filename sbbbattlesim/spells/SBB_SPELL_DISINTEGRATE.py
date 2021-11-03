import random

from sbbbattlesim import utils
from sbbbattlesim.spells import NonTargetedSpell, TargetedSpell


class SpellType(TargetedSpell):
    display_name = 'Smite'
    level = 0
    spell_filter = ()

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=-30, temp=False, reason=f'{self} effect')