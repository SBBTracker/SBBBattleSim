import random

from sbbbattlesim.spells import NonTargetedSpell


class SpellType(NonTargetedSpell):
    display_name = 'Earthquake'
    level = 0
    spell_filter = ()

    def cast(self, player, *args, **kwargs):
        for char in player.opponent.valid_characters(_lambda=lambda char: char.position in (1, 2, 3, 4)):
            char.change_stats(damage=1, reason=f'{self} damage')