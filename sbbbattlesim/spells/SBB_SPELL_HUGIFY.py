from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = 'Hugeify'
    _level = 6
    cost = 4
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        Buff(targets=[target], attack=10, temp=False, reason=ActionReason.HUGEIFY, source=self, *args, **kwargs)
