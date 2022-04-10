from sbbbattlesim.spells import Spell
from sbbbattlesim.action import ActionReason, Buff


class SpellType(Spell):
    display_name = 'Gigantify'
    _level = 6
    cost = 4
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        Buff(targets=[target], health=10, temp=False, reason=ActionReason.GIGANTIFY, source=self, *args, **kwargs)
