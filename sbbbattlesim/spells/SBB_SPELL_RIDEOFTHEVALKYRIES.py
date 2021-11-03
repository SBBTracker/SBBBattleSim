import random

from sbbbattlesim.spells import NonTargetedSpell


class SpellType(NonTargetedSpell):
    display_name = 'Ride of the Valkyries'
    level = 0
    spell_filter = ()

    def cast(self, player, *args, **kwargs):
        for char in player.valid_characters():
            char.change_stats(attack=3, temp=False, reason=f'{self} buff')