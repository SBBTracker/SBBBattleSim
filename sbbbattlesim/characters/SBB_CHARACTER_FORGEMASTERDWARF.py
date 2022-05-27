import logging

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class LordyBuffOnStart(OnStart):
    def handle(self, stack, *args, **kwargs):
        dwarfes = self.source.player.valid_characters(
            _lambda=lambda char: Tribe.DWARF in char.tribes
        )
        stat_change = len(dwarfes) * (4 if self.source.golden else 2)
        Buff(reason=ActionReason.LORDY_BUFF, source=self.source, targets=dwarfes,
             attack=stat_change, health=stat_change, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Lordy'

    _attack = 7
    _health = 7
    _level = 6
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(LordyBuffOnStart, priority=90, source=self)
