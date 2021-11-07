import random

from sbbbattlesim.spells import TargetedSpell


class SpellType(TargetedSpell):
    display_name = '''Luna's Grave'''
    spell_type = ('evil')

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=3, attack=3, temp=False, reason=f'{self} buff')