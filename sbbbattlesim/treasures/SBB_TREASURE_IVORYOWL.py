import logging

from sbbbattlesim import utils
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath, OnStart
from sbbbattlesim.utils import StatChangeCause

logger = logging.getLogger(__name__)


class TreasureType(Treasure):
    display_name = 'Ivory Owl'

    _level = 6

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class IvoryOwlOnStartOnStartBuff(OnStart):
            owl = self
            def handle(self, stack, *args, **kwargs):
                for _ in range(bool(self.owl.mimic) + 1):
                    for char in self.manager.valid_characters():
                        char.change_stats(attack=2, health=2, reason=StatChangeCause.IVORY_OWL_BUFF, source=self.owl, temp=False, stack=stack)

        self.player.register(IvoryOwlOnStartOnStartBuff)
