from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import Tribe


# todo implement this if it can ever get cast in combat
class SpellType(TargetedSpell):
    display_name = '''Evil Twin'''
    _level = 6

    def cast(self, target, *args, **kwargs):
        pass

    def filter(self, char):
        return Tribe.GOOD in char.tribes
