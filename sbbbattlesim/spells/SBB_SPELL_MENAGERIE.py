import random

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Toil and Trouble'''
    _level = 4
    cost = 2

    def cast(self, target: 'Character' = None, *args, **kwargs):
        valid_targets = self.player.valid_characters()
        if len(valid_targets):
            targets = random.sample(valid_targets, min(len(valid_targets), 2))
            Buff(reason=ActionReason.TOIL_AND_TROUBLE, source=self, targets=targets,
                 health=2, attack=2, temp=False, *args, **kwargs).resolve()
