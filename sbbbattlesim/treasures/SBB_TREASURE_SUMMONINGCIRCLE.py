import logging

from sbbbattlesim.events import OnSummon
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause

logger = logging.getLogger(__name__)


class SummoningPortalBuff(OnSummon):
    def handle(self, summoned_characters, stack, *args, **kwargs):
        for char in sorted(summoned_characters, key=lambda char: char.position, reverse=True):
            logger.debug(f'IS CHARACTER THE CHARACTER {char is self.manager.characters[char.position]}')
            self.portal.buff_count += 1
            for _ in range(self.portal.mimic + 1):
                char.change_stats(attack=self.portal.buff_count, health=self.portal.buff_count,
                                  reason=StatChangeCause.SUMMONING_PORTA, source=self.portal, temp=False,
                                  stack=stack)


class TreasureType(Treasure):
    display_name = 'Summoning Portal'

    _level = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buff_count = 0
        self.player.register(SummoningPortalBuff, portal=self)
