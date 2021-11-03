import random

from sbbbattlesim import utils
from sbbbattlesim.spells import NonTargetedSpell


class SpellType(NonTargetedSpell):
    display_name = 'Fireball'
    level = 0
    spell_filter = ()

    def cast(self, player, *args, **kwargs):
        target = random.choice(player.opponent.valid_characters(_lambda=lambda char: char.position in (1, 2, 3, 4)))
        if target is not None:
            target.change_stats(damage=10, reason=f'{self} damage')
            for behind_position in utils.get_behind_targets(target.position):
                behind_target = player.opponent.characters(behind_position)
                if behind_target is not None:
                    behind_target.change_stats(damage=10, reason=f'{self} damage')