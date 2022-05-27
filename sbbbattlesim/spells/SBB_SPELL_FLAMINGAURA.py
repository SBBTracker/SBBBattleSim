from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = 'Burning Palm'
    _level = 4
    cost = 2
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        Buff(attack=4, temp=False, reason=ActionReason.STONE_SKIN, source=self, targets=[target], *args, **kwargs)
