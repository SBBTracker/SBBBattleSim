from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import Tribe


class SpellType(TargetedSpell):
    display_name = 'Worm Root'
    _level = 3

    def cast(self, target, *args, **kwargs):
        Buff(targets=[target], attack=3, health=3, temp=False, reason=ActionReason.WORM_ROOT, source=self, *args, **kwargs)

    def filter(self, char):
        return Tribe.MONSTER in char.tribes
