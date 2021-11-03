import random

from sbbbattlesim.spells import NonTargetedSpell


class SpellType(NonTargetedSpell):
    display_name = 'Blessing of Athena'
    level = 0
    spell_filter = ()

    def cast(self, player, *args, **kwargs):
        for char in player.valid_characters():
            char.change_stats(attack=1, health=1, temp=False, reason=f'{self} buff')