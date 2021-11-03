import random

from sbbbattlesim import utils
from sbbbattlesim.spells import NonTargetedSpell, TargetedSpell


class SpellType(TargetedSpell):
    display_name = 'Shrivel'
    level = 0
    spell_filter = ()

    def cast(self, target, *args, **kwargs):
        target.change_stats(attack=-12, health=-12, temp=False, reason=f'{self} effect')