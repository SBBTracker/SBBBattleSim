import logging

from sbbbattlesim.events import OnSummon
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.characters import registry as character_registry

logger = logging.getLogger(__name__)


class ReduplicatorOnSummon(OnSummon):
    def handle(self, summoned_characters, *args, **kwargs):
        if summoned_characters and not self.source.triggered:
            if len(self.manager.valid_characters()) != 7:
                logger.debug(f'YO IM SO TRIGGERED')
                self.source.triggered = True
                for _ in range(self.source.mimic + 1):
                    new_char = summoned_characters[-1].copy()
                    self.manager.summon(new_char.position, [new_char], *args, **kwargs)


class TreasureType(Treasure):
    display_name = 'Reduplicator'

    _level = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered = False
        self.player.register(ReduplicatorOnSummon, source=self, priority=-10)
