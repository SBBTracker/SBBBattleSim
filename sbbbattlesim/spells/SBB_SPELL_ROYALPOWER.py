from sbbbattlesim.action import Buff
from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause, Tribe


class SpellType(TargetedSpell):
    display_name = '''Queen's Grace'''
    _level = 4

    def cast(self, target, *args, **kwargs):
        Buff(targets=[target], health=7, attack=7, temp=False, reason=StatChangeCause.QUEENS_GRACE, source=self, *args, **kwargs)

    def filter(self, char):
        return Tribe.PRINCESS in char.tribes or Tribe.PRINCE in char.tribes
