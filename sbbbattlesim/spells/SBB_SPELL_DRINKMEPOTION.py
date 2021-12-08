from sbbbattlesim.action import Buff
from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = '''Luna's Grace'''
    _level = 3

    def cast(self, target, *args, **kwargs):
        Buff(reason=StatChangeCause.LUNAS_GRAVE, source=self, targets=[target],
             health=3, attack=3, temp=False,  *args, **kwargs).resolve()
