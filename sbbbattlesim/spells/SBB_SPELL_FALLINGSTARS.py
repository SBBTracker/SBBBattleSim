import random

from sbbbattlesim.spells import NonTargetedSpell


class SpellType(NonTargetedSpell):
    display_name = 'Falling Stars'
    level = 0
    spell_filter = ()

    def cast(self, player, *args, **kwargs):
        for char in player.valid_characters() + player.opponent.valid_characters():
            char.change_stats(damage=1, reason=f'{self} damage')