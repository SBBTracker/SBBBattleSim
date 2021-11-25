import random

from sbbbattlesim import utils
from sbbbattlesim.damage import Damage
from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(NonTargetedSpell):
    display_name = 'Fireball'
    _level = 4

    def cast(self, player, *args, **kwargs):
        valid_targets = player.opponent.valid_characters(_lambda=lambda char: char.position in (1, 2, 3, 4))
        if valid_targets:
            target = random.choice(valid_targets)
            targets = [target]
            for behind_position in utils.get_behind_targets(target.position):
                char = player.opponent.characters.get(behind_position)
                if char:
                    targets.append(char)

            Damage(10, reason=StatChangeCause.FIREBALL, source=self, targets=targets).resolve()
