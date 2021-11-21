import random

from sbbbattlesim import utils
from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(NonTargetedSpell):
    display_name = 'Fireball'
    level = 0

    def cast(self, player, *args, **kwargs):
        valid_targets = player.opponent.valid_characters(_lambda=lambda char: char.position in (1, 2, 3, 4))
        if valid_targets:
            target = random.choice(valid_targets)
            if target is not None:
                target.change_stats(damage=10, reason=StatChangeCause.FIREBALL, source=self)
                for behind_position in utils.get_behind_targets(target.position):
                    behind_target = player.opponent.characters.get(behind_position)
                    if behind_target is not None:
                        behind_target.change_stats(damage=10, reason=StatChangeCause.FIREBALL, source=self)