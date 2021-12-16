from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.action import ActionReason


class SpellType(TargetedSpell):
    display_name = 'Gigantify'
    _level = 6

    def cast(self, target, *args, **kwargs):
        Buff(targets=[target], health=10, temp=False, reason=ActionReason.GIGANTIFY, source=self, *args, **kwargs)
