import random

from sbbbattlesim.action import Damage, ActionReason
from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = 'Shrivel'
    _level = 5
    cost = 2

    def cast(self, target: 'Character' = None, *args, **kwargs):
        valid_targets = self.player.opponent.valid_characters()
        if valid_targets:
            target = random.choice(valid_targets)
            # target.change_stats(attack=-12, health=-12, temp=False, reason=StatChangeCause.SHRIVEL, source=self, *args, **kwargs)
            Damage(
                damage=0,
                targets=[target],
                reason=ActionReason.SHRIVEL,
                source=self,
                attack=-12,
                health=-12,
                temp=False,
                *args, **kwargs
            ).resolve()
