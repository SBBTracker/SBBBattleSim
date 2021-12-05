import logging

from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause

logger = logging.getLogger(__name__)


class TreasureType(Treasure):
    display_name = 'Other Hand of Vekna'
    aura = True

    _level = 4

    def buff(self, target_character, *args, **kwargs):
        class OtherHandOfVekna(OnDeath):
            last_breath = False
            vekna = self

            def handle(self, stack, *args, **kwargs):
                positions = (1, 2, 3, 4) if self.manager.position in (1, 2, 3, 4) else (5, 6, 7)
                for char in self.manager.owner.valid_characters(_lambda=lambda char: char.position in positions):
                    char.change_stats(health=1, attack=1, reason=StatChangeCause.OTHER_HAND_OF_VEKNA,
                                      source=self.vekna, temp=False, stack=stack)
                    if self.vekna.mimic:
                        char.change_stats(health=1, attack=1, reason=StatChangeCause.OTHER_HAND_OF_VEKNA,
                                          source=self.vekna, temp=False, stack=stack)

        target_character.register(OtherHandOfVekna, temp=True)
