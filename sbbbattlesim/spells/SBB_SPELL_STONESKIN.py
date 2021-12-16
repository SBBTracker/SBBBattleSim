from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.action import ActionReason


class SpellType(TargetedSpell):
    display_name = 'Stoneskin'
    _level = 4

    def cast(self, target, *args, **kwargs):
        Buff(targets=[target], health=4, temp=False, reason=ActionReason.STONE_SKIN, source=self, *args, **kwargs)
