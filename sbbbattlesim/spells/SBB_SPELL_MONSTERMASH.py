from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause, Tribe


class SpellType(TargetedSpell):
    display_name = 'Worm Root'

    def cast(self, target, *args, **kwargs):
        target.change_stats(attack=10, temp=False, reason=StatChangeCause.WORM_ROOT, source=self)

    def filter(self, char):
        return Tribe.MONSTER in char.tribes