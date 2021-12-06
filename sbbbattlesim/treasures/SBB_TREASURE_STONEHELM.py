import logging

from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause

logger = logging.getLogger(__name__)


class TreasureType(Treasure):
    display_name = 'Haunted Helm'
    aura = True

    _level = 3

    def buff(self, target_character, *args, **kwargs):
        if target_character.position == 1:
            for _ in range(self.mimic + 1):
                target_character.change_stats(health=10, reason=StatChangeCause.STONEHELM, source=self, temp=True,
                                              *args, **kwargs)
