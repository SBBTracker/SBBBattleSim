from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import TargetedSpell


class SpellType(TargetedSpell):
    display_name = '''Luna's Grace'''
    _level = 3

    def cast(self, target, *args, **kwargs):
        Buff(reason=ActionReason.LUNAS_GRAVE, source=self, targets=[target],
             health=3, attack=3, temp=False, *args, **kwargs).resolve()
