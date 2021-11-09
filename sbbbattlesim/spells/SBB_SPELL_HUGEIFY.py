from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = 'Hugeify'

    def cast(self, target, *args, **kwargs):
        target.change_stats(attack=10, temp=False, reason=StatChangeCause.HUGEIFY, source=self)