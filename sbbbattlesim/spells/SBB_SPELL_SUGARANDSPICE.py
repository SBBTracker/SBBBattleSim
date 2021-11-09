import random

from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause, Tribe


class SpellType(TargetedSpell):
    display_name = 'Sugar and Spice'

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=1, attack=1, temp=False, reason=StatChangeCause.SUGAR_AND_SPICE, source=self)

    def filter(self, char):
        return Tribe.GOOD in char.tribes