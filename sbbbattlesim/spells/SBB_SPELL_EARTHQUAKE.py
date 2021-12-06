import logging

from sbbbattlesim.damage import Damage
from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.utils import StatChangeCause

logger = logging.getLogger(__name__)


class SpellType(NonTargetedSpell):
    display_name = 'Earthquake'
    _level = 3

    def cast(self, player, *args, **kwargs):
        targets = player.opponent.valid_characters(_lambda=lambda char: char.position in (1, 2, 3, 4))
        Damage(2, reason=StatChangeCause.EARTHQUAKE, source=self, targets=targets).resolve()
