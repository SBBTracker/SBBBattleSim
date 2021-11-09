import random

from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(NonTargetedSpell):
    display_name = 'Falling Stars'
    level = 0

    def cast(self, player, *args, **kwargs):
        for char in player.valid_characters() + player.opponent.valid_characters():
            char.change_stats(damage=1, reason=StatChangeCause.FALLING_STARS, source=self)