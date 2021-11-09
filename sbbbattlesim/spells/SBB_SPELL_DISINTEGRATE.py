import random

from sbbbattlesim import utils
from sbbbattlesim.spells import NonTargetedSpell, TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = 'Smite'
    level = 0

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=-30, temp=False, reason=StatChangeCause.SMITE, source=self)