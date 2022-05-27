from sbbbattlesim.spells import Spell
from sbbbattlesim.utils import Tribe


# todo implement this if it can ever get cast in combat
class SpellType(Spell):
    display_name = '''Evil Twin'''
    _level = 6
    cost = 8
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass

    @classmethod
    def filter(cls, char):
        return Tribe.GOOD in char.tribes
