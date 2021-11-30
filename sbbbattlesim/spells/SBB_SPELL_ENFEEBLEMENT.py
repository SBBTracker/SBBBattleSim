from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = 'Shrivel'
    _level = 5

    def cast(self, target, *args, **kwargs):
        target.change_stats(attack=-12, health=-12, temp=False, reason=StatChangeCause.SHRIVEL, source=self, stack=None)