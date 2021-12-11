import logging

from sbbbattlesim.action import Buff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause

logger = logging.getLogger(__name__)


class TreasureType(Treasure):
    display_name = 'Cloak of the Assassin'
    aura = True

    _level = 3

    def buff(self, target_character, *args, **kwargs):
        logger.debug(f'IS THIS A SLAY??? {target_character}  {target_character.slay}')
        if target_character.slay:
            for _ in range(self.mimic + 1):
                Buff(reason=StatChangeCause.CLOAK_OF_THE_ASSASSIN, source=self, targets=[target_character],
                     health=3, attack=3,  temp=True, *args, **kwargs).resolve()
