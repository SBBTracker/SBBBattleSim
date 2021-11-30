from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = '''Luna's Grace'''
    _level = 3

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=3, attack=3, temp=False, reason=StatChangeCause.LUNAS_GRAVE, source=self, stack=None)