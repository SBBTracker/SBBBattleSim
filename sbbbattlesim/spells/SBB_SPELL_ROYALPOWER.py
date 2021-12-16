from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import Tribe


class SpellType(TargetedSpell):
    display_name = '''Queen's Grace'''
    _level = 4

    def cast(self, target, *args, **kwargs):
        Buff(targets=[target], health=7, attack=7, temp=False, reason=ActionReason.QUEENS_GRACE, source=self, *args, **kwargs)

    def filter(self, char):
        return Tribe.PRINCESS in char.tribes or Tribe.PRINCE in char.tribes
