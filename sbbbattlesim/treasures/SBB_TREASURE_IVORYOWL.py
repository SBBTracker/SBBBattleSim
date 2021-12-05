import logging

from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause

logger = logging.getLogger(__name__)


class TreasureType(Treasure):
    display_name = 'Ivory Owl'

    _level = 6

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class IvoryOwlOnStartOnStartBuff(OnStart):
            priority = 120
            owl = self

            def handle(self, stack, *args, **kwargs):
                for _ in range(bool(self.owl.mimic) + 1):
                    for char in self.owl.player.valid_characters():
                        char.change_stats(attack=2, health=2, reason=StatChangeCause.IVORY_OWL_BUFF, source=self.owl, temp=False, stack=stack)

        self.player.board.register(IvoryOwlOnStartOnStartBuff)
