import logging
import random

from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.utils import StatChangeCause

logger = logging.getLogger(__name__)


class SpellType(NonTargetedSpell):
    display_name = 'Earthquake'
    level = 0

    def cast(self, player, *args, **kwargs):
        for char in player.opponent.valid_characters(_lambda=lambda char: char.position in (1, 2, 3, 4)):
            char.change_stats(damage=1, reason=StatChangeCause.EARTHQUAKE, source=self)