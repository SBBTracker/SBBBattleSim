import logging

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure

logger = logging.getLogger(__name__)


class TreasureType(Treasure):
    display_name = 'Sting'
    aura = True

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 10 * (self.mimic + 1)
        self.aura = Aura(reason=ActionReason.STING, source=self, attack=stats,
                              _lambda=lambda char: char.position == 1)

    
