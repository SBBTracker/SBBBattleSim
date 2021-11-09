import random

from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(NonTargetedSpell):
    display_name = 'Blessing of Athena'
    level = 0

    def cast(self, player, *args, **kwargs):
        for char in player.valid_characters():
            char.change_stats(attack=1, health=1, temp=False, reason=StatChangeCause.BLESSING_OF_ATHENA, source=self)