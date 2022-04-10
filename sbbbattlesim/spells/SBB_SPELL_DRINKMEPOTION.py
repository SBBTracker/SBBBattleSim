from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Luna's Grace'''
    _level = 3
    targeted = True
    cost = 1

    def cast(self, target: 'Character' = None, *args, **kwargs):
        Buff(reason=ActionReason.LUNAS_GRAVE, source=self, targets=[target],
             health=3, attack=3, temp=False, *args, **kwargs).resolve()
