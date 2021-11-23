import random

from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause, Tribe

#todo implement this if it can ever get cast in combat
class SpellType(TargetedSpell):
    display_name = '''Evil Twin'''

    def cast(self, target, *args, **kwargs):
        pass

    def filter(self, char):
        return Tribe.GOOD in char.tribes
