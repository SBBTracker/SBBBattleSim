import random

from sbbbattlesim import utils
from sbbbattlesim.action import Damage, ActionReason
from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = 'Fireball'
    _level = 4
    cost = 0

    def cast(self, target: 'Character' = None, *args, **kwargs):
        valid_targets = self.player.opponent.valid_characters(_lambda=lambda char: char.position in (1, 2, 3, 4))
        if not valid_targets:
            valid_targets = self.player.opponent.valid_characters(_lambda=lambda char: char.position in (5, 6, 7))

        if valid_targets:
            target = random.choice(valid_targets)
            targets = [target]
            for behind_position in utils.get_behind_targets(target.position):
                char = self.player.opponent.characters.get(behind_position)
                if char:
                    targets.append(char)

            # TODO figure out if it goes left/right or right/left
            Damage(damage=3, reason=ActionReason.FIREBALL, source=self, targets=targets).resolve()
