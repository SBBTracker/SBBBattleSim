from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = 'Magic Research'

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=1, attack=1, temp=False, reason=StatChangeCause.MAGIC_RESEARCH, source=self)