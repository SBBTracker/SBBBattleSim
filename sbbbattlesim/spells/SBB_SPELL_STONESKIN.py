from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = 'Stoneskin'
    _level = 4

    def cast(self, target, *args, **kwargs):
        Buff(targets=[target], health=4, temp=False, reason=StatChangeCause.STONE_SKIN, source=self, *args, **kwargs)
