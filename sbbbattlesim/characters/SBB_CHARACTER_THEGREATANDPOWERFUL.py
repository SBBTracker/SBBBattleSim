from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSpellCast, OnStart, OnSummon
from sbbbattlesim.utils import StatChangeCause, Tribe
import logging

logger = logging.getLogger(__name__)

class StormKingOnStart(OnStart):
    def handle(self, stack, *args, **kwargs):
        current_buff = self.storm_king.player._spells_cast

        current_attack = int(
            (self.storm_king.attack - (self.storm_king._attack * (2 if self.storm_king.golden else 1))) / (
                4 if self.storm_king.golden else 2))
        current_health = int(
            (self.storm_king.health - (self.storm_king._health * (2 if self.storm_king.golden else 1))) / (
                4 if self.storm_king.golden else 2))

        new_buff = min(current_attack, current_health)

        self.storm_king.player._spells_cast = min(current_buff, new_buff) if current_buff is not None else new_buff


class StormKingOnSummon(OnSummon):
    def handle(self, summoned_characters, stack, *args, **kwargs):
        if not self.storm_king in summoned_characters:
            return

        spells_cast = self.storm_king.player._spells_cast

        golden_multipler = 4 if self.storm_king.golden else 2
        storm_king_buff = (spells_cast or 0) * golden_multipler

        Buff(reason=StatChangeCause.STORM_KING_BUFF, source=self.storm_king, targets=[self.storm_king],
             attack=storm_king_buff, health=storm_king_buff, temp=False).resolve()


class StormKingOnSpellCast(OnSpellCast):
    def handle(self, stack, *args, **kwargs):
        stat_buff = 4 if self.storm_king.golden else 2

        Buff(reason=StatChangeCause.STORM_KING_BUFF, source=self.storm_king, targets=[self.storm_king],
             attack=stat_buff, health=stat_buff, temp=False, *args, **kwargs).resolve()


class CharacterType(Character):
    # TODO this needs to be changed after the resolve_board removal
    display_name = 'Storm King'

    _attack = 2
    _health = 2
    _level = 6
    _tribes = {Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.player.register(StormKingOnSpellCast, storm_king=self)
        self.player.register(StormKingOnSummon, storm_king=self, priority=-15)
        self.player.board.register(StormKingOnStart, storm_king=self, priority=9000)

    @classmethod
    def new(cls, *args, **kwargs):
        self = super().new(*args, **kwargs)

        # TODO add this back in later
        # self.player.resolve_board()
        #
        # stat_buff = self.player._spells_cast * (4 if self.golden else 2)
        #
        # self.change_stats(
        #     attack=stat_buff,
        #     health=stat_buff,
        #     reason=StatChangeCause.STORM_KING_BUFF,
        #     source=self,
        # )

        return self
