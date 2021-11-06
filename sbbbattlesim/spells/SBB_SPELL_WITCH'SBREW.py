import random

from sbbbattlesim.spells import TargetedSpell


class SpellType(TargetedSpell):
    display_name = '''Witch's Brew'''
    spell_type = ('evil')

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=1, attack=1, temp=False, reason=f'{self} buff')