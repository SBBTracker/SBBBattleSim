import logging

from sbbbattlesim.action import Buff, ActionReason, Aura, ActionState
from sbbbattlesim.events import OnBuff, OnSpawn, OnSummon
from sbbbattlesim.treasures import Treasure

logger = logging.getLogger(__name__)

class TreasureType(Treasure):
    display_name = 'Singing Swords'
    _level = 6
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 15 * (self.mimic + 1)
        self.aura = Aura(reason=ActionReason.SINGINGSWORD_BUFF, source=self, attack=stats,
                         _lambda=lambda char: char.position in (1, 2, 3, 4), )
