import logging

from sbbbattlesim.action import Buff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause

logger = logging.getLogger(__name__)


class TreasureType(Treasure):
    display_name = 'Sting'
    aura = True

    _level = 3

    def buff(self, target_character, *args, **kwargs):
        if target_character.position == 1:
            for _ in range(self.mimic + 1):
                Buff(reason=StatChangeCause.STING, source=self, targets=[target_character],
                     attack=10,  temp=True, *args, **kwargs).resolve()
