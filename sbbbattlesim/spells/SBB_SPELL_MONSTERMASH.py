from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause, Tribe


class SpellType(TargetedSpell):
    display_name = 'Worm Root'
    _level = 3

    def cast(self, target, *args, **kwargs):
        target.change_stats(attack=3, health=3, temp=False, reason=StatChangeCause.WORM_ROOT, source=self, stack=None)

    def filter(self, char):
        return Tribe.MONSTER in char.tribes