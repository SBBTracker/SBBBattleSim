import logging

from sbbbattlesim.action import Buff, AuraBuff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause

logger = logging.getLogger(__name__)


class TreasureType(Treasure):
    display_name = 'Sting'
    aura = True

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 10 * (self.mimic + 1)
        self.aura_buff = AuraBuff(reason=StatChangeCause.STING, source=self, attack=stats,
                                  _lambda=lambda char: char.position == 1)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
