import random

from sbbbattlesim import utils
from sbbbattlesim.spells import NonTargetedSpell, TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = 'Poison Apple'
    level = 5

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=-target._base_health, temp=False, reason=StatChangeCause.POISON_APPLE, source=self)