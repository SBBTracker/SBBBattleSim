from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import Spell
from sbbbattlesim.utils import Tribe


class SpellType(Spell):
    display_name = 'Flourish'
    _level = 3
    cost = 2
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        Buff(targets=[target], health=7, temp=False, reason=ActionReason.FLOURISH, source=self, *args, **kwargs)

    @classmethod
    def filter(cls, char):
        return Tribe.TREANT in char.tribes
