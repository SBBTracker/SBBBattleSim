from sbbbattlesim.spells import Spell
from sbbbattlesim.action import ActionReason
from sbbbattlesim.action import Buff


class SpellType(Spell):
    display_name = 'Genies\s Wish'
    _level = 2
    cost = 1

    def cast(self, target: 'Character' = None, *args, **kwargs):
        Buff(targets=[target], attack=10, temp=False, reason=ActionReason.HUGEIFY, source=self, *args, **kwargs)
