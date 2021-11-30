from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = 'Burning Palm'
    _level = 4

    def cast(self, target, *args, **kwargs):
        target.change_stats(attack=4, temp=False, reason=StatChangeCause.STONE_SKIN, source=self, stack=None)