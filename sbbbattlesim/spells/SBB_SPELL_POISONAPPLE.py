from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = 'Poison Apple'
    _level = 5

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=-target._base_health, temp=False, reason=StatChangeCause.POISON_APPLE, source=self)