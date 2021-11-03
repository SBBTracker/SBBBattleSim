import random

from sbbbattlesim.spells import TargetedSpell


class SpellType(TargetedSpell):
    display_name = 'Sugar and Spice'
    spell_type = ('good')

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=1, attack=1, temp=False, reason=f'{self} buff')