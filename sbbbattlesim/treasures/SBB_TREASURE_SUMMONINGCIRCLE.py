import logging

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.events import OnSummon
from sbbbattlesim.treasures import Treasure

logger = logging.getLogger(__name__)


class SummoningPortalBuff(OnSummon):
    def handle(self, summoned_characters, stack, *args, **kwargs):
        for char in summoned_characters:
            self.source.buff_count += 1
            buff = self.source.buff_count * (1 + self.source.multiplier)
            Buff(reason=ActionReason.SUMMONING_PORTA, source=self.source, attack=buff, health=buff, stack=stack).execute(char)


class TreasureType(Treasure):
    display_name = 'Summoning Portal'
    _level = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buff_count = 0
        self.player.register(SummoningPortalBuff, source=self, priority=-10)
