from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import Tribe


class SpellType(TargetedSpell):
    display_name = 'Sugar and Spice'
    _level = 2

    def cast(self, target, *args, **kwargs):
        Buff(targets=[target], health=1, attack=1, temp=False, reason=ActionReason.SUGAR_AND_SPICE, source=self, *args, **kwargs)

    def filter(self, char):
        return Tribe.GOOD in char.tribes
