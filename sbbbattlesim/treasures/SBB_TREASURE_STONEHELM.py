import logging

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure

logger = logging.getLogger(__name__)


class TreasureType(Treasure):
    display_name = 'Haunted Helm'
    aura = True

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 10 * (self.multiplier + 1)
        self.aura = Aura(reason=ActionReason.STONEHELM, source=self, health=stats,
                         _lambda=lambda char: char.position == 1)
