from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import Spell
from sbbbattlesim.utils import Tribe


class SpellType(Spell):
    display_name = 'Sugar and Spice'
    _level = 2
    cost = 1
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        Buff(targets=[target], health=1, attack=1, temp=False, reason=ActionReason.SUGAR_AND_SPICE, source=self, *args,
             **kwargs)

    @classmethod
    def filter(cls, char):
        return Tribe.GOOD in char.tribes
