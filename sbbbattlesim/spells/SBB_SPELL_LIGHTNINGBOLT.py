import random

from sbbbattlesim.spells import NonTargetedSpell


class SpellType(NonTargetedSpell):
    display_name = 'Lightning Bolt'
    level = 0
    spell_filter = ()

    def cast(self, player, *args, **kwargs):
        target = random.choice(player.opponent.valid_characters(_lambda=lambda char: char.position in (5, 6, 7)))
        if target is not None:
            target.change_stats(damage=10, reason=f'{self} damage')
