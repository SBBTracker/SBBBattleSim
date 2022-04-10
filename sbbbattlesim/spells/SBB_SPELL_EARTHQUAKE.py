import logging

from sbbbattlesim.action import Damage, ActionReason
from sbbbattlesim.spells import Spell

logger = logging.getLogger(__name__)


class SpellType(Spell):
    display_name = 'Earthquake'
    _level = 3
    cost = 1

    def cast(self, target: 'Character' = None, *args, **kwargs):
        targets = self.player.opponent.valid_characters(_lambda=lambda char: char.position in (1, 2, 3, 4))
        Damage(damage=2, reason=ActionReason.EARTHQUAKE, source=self, targets=targets).resolve()
