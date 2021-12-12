import logging

from sbbbattlesim.action import Buff
from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause

logger = logging.getLogger(__name__)


class OtherHandOfVekna(OnDeath):
    last_breath = False

    def handle(self, stack, *args, **kwargs):
        positions = (1, 2, 3, 4) if self.manager.position in (1, 2, 3, 4) else (5, 6, 7)
        targets = self.manager.player.valid_characters(_lambda=lambda char: char.position in positions)
        for _ in range(self.vekna.mimic + 1):
            Buff(reason=StatChangeCause.OTHER_HAND_OF_VEKNA, source=self.vekna, targets=targets,
                 health=1, attack=1,  temp=False, stack=stack).resolve()


class TreasureType(Treasure):
    display_name = 'Other Hand of Vekna'
    aura = True

    _level = 4

    def buff(self, target_character, *args, **kwargs):
        target_character.register(OtherHandOfVekna, temp=True, vekna=self)
