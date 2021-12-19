import logging

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.events import OnSummon
from sbbbattlesim.treasures import Treasure

logger = logging.getLogger(__name__)


class SummoningPortalBuff(OnSummon):
    def handle(self, summoned_characters, stack, *args, **kwargs):
        for char in summoned_characters:
            self.source.buff_count += 1
            for _ in range(self.source.mimic + 1):
                Buff(reason=ActionReason.SUMMONING_PORTA, source=self.source, targets=[char],
                     attack=self.source.buff_count, health=self.source.buff_count, stack=stack).resolve()


class TreasureType(Treasure):
    display_name = 'Summoning Portal'

    _level = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buff_count = 0
        self.player.register(SummoningPortalBuff, source=self)
