import random

from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause, Tribe


class SpellType(TargetedSpell):
    display_name = '''Beauty's Influence'''

    def cast(self, target, *args, **kwargs):
        pass

    def filter(self, char):
        return Tribe.GOOD in char.tribes
