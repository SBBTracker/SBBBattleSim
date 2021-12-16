import logging

from sbbbattlesim.action import Damage, ActionReason
from sbbbattlesim.spells import NonTargetedSpell

logger = logging.getLogger(__name__)


class SpellType(NonTargetedSpell):
    display_name = 'Earthquake'
    _level = 3

    def cast(self, player, *args, **kwargs):
        targets = player.opponent.valid_characters(_lambda=lambda char: char.position in (1, 2, 3, 4))
        Damage(damage=2, reason=ActionReason.EARTHQUAKE, source=self, targets=targets).resolve()
