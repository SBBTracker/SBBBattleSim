import random

from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(NonTargetedSpell):
    display_name = 'Lightning Bolt'
    level = 4

    def cast(self, player, *args, **kwargs):
        valid_targets = player.opponent.valid_characters(_lambda=lambda char: char.position in (5, 6, 7))
        if valid_targets:
            target = random.choice(valid_targets)
            if target is not None:
                target.change_stats(damage=10, reason=StatChangeCause.LIGHTNING_BOLT, source=self)
