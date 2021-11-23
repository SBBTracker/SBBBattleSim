import random

from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(NonTargetedSpell):
    display_name = 'Ride of the Valkyries'
    level = 4

    def cast(self, player, *args, **kwargs):
        for char in player.valid_characters():
            char.change_stats(attack=3, temp=False, reason=StatChangeCause.RIDE_OF_THE_VALKYRIES, source=self)