from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = 'Smite'
    _level = 6

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=-30, temp=False, reason=StatChangeCause.SMITE, source=self, stack=None)