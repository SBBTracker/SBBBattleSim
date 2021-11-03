import random

from sbbbattlesim import utils
from sbbbattlesim.spells import NonTargetedSpell, TargetedSpell


class SpellType(TargetedSpell):
    display_name = 'Poison Apple'
    level = 0
    spell_filter = ()

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=-target._base_health, temp=False, reason=f'{self} effect')