from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import TargetedSpell


class SpellType(TargetedSpell):
    display_name = 'Burning Palm'
    _level = 4

    def cast(self, target, *args, **kwargs):
        Buff(attack=4, temp=False, reason=ActionReason.STONE_SKIN, source=self, targets=[target], *args, **kwargs)
