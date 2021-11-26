import logging

from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnSummon
from sbbbattlesim.utils import StatChangeCause

logger = logging.getLogger(__name__)


class TreasureType(Treasure):
    display_name = 'Summoning Portal'

    _level = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buff_count = 0

        class SummoningPortalBuff(OnSummon):
            portal = self
            def handle(self, summoned_characters, *args, **kwargs):
                for char in sorted(summoned_characters, key=lambda char: char.position, reverse=True):
                    logger.debug(f'IS CHARACTER THE CHARACTER {char is self.manager.characters[char.position]}')
                    self.portal.buff_count += 1
                    char.change_stats(attack=self.portal.buff_count, health=self.portal.buff_count,
                                      reason=StatChangeCause.SUMMONING_PORTA, source=self.portal, temp=False)
                    if self.portal.mimic:
                        char.change_stats(attack=self.portal.buff_count, health=self.portal.buff_count,
                                          reason=StatChangeCause.SUMMONING_PORTA, source=self.portal, temp=False)

        self.player.register(SummoningPortalBuff)

