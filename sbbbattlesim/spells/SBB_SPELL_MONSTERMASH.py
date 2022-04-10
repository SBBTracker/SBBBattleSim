from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import Spell
from sbbbattlesim.utils import Tribe


class SpellType(Spell):
    display_name = 'Worm Root'
    _level = 3
    cost = 2
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        Buff(targets=[target], attack=3, health=3, temp=False, reason=ActionReason.WORM_ROOT, source=self, *args,
             **kwargs)

    @classmethod
    def filter(cls, char):
        return Tribe.MONSTER in char.tribes
