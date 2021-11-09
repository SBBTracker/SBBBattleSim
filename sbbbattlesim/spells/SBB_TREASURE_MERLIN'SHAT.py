from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = 'Stoneskin'

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=4, attack=4, temp=False, reason=StatChangeCause.MERLINS_TEST, source=self)