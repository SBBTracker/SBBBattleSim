import random

from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = '''Luna's Grave'''

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=3, attack=3, temp=False, reason=StatChangeCause.LUNAS_GRAVE, source=self)