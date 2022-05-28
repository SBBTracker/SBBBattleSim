import logging

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure

logger = logging.getLogger(__name__)


class IvoryOwlOnStartOnStartBuff(OnStart):
    def handle(self, stack, *args, **kwargs):
        for _ in range(bool(self.source.mimic) + 1):
            Buff(reason=ActionReason.IVORY_OWL_BUFF, source=self.source, targets=self.source.player.valid_characters(),
                 attack=2, health=2, stack=stack).resolve()


class TreasureType(Treasure):
    display_name = 'Ivory Owl'

    _level = 6

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.player.register(IvoryOwlOnStartOnStartBuff, priority=120, source=self)
