from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import Tribe


class SpellType(TargetedSpell):
    display_name = 'Flourish'
    _level = 3

    def cast(self, target, *args, **kwargs):
        Buff(targets=[target], health=7, temp=False, reason=ActionReason.FLOURISH, source=self, *args, **kwargs)

    def filter(self, char):
        return Tribe.TREANT in char.tribes
