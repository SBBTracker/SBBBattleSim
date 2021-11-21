import logging

from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


logger = logging.getLogger(__name__)


class TreasureType(Treasure):
    display_name = 'Sting'
    aura = True

    def buff(self, target_character):
        if target_character.position == 1:
            logger.debug(f'STING MIMIC COUNTER IS {self.mimic}')
            for _ in range(self.mimic + 1):
                target_character.change_stats(attack=10, reason=StatChangeCause.STING, source=self, temp=True)
