import logging

from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import StatChangeCause, Tribe

logger = logging.getLogger(__name__)


class LordyBuffOnStart(OnStart):
    def handle(self, stack, *args, **kwargs):
        dwarfes = self.lordy.player.valid_characters(
            _lambda=lambda char: Tribe.DWARF in char.tribes or char.id == 'SBB_CHARACTER_PRINCESSNIGHT'
        )
        stat_change = len(dwarfes) * (4 if self.lordy.golden else 2)
        Buff(reason=StatChangeCause.LORDY_BUFF, source=self.lordy, targets=dwarfes,
             attack=stat_change, health=stat_change, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Lordy'

    _attack = 7
    _health = 7
    _level = 6
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.board.register(LordyBuffOnStart, priority=90, lordy=self)
