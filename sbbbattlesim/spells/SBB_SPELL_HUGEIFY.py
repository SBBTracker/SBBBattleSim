from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import TargetedSpell


class SpellType(TargetedSpell):
    display_name = 'Hugeify'
    _level = 6

    def cast(self, target, *args, **kwargs):
        Buff(targets=[target], attack=10, temp=False, reason=ActionReason.HUGEIFY, source=self, *args, **kwargs)
