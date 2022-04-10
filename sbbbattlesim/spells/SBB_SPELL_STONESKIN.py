from sbbbattlesim.spells import Spell
from sbbbattlesim.action import ActionReason


class SpellType(Spell):
    display_name = 'Stoneskin'
    _level = 4
    cost = 2
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        Buff(targets=[target], health=4, temp=False, reason=ActionReason.STONE_SKIN, source=self, *args, **kwargs)
