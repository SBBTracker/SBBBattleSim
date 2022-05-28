from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSpellCast, OnStart, OnSummon
from sbbbattlesim.utils import Tribe
import logging

logger = logging.getLogger(__name__)


class StormKingOnStart(OnStart):
    def handle(self, stack, *args, **kwargs):
        current_buff = self.source.player._spells_cast

        current_attack = int(
            (self.source.attack - (self.source._attack * (2 if self.source.golden else 1))) / (
                4 if self.source.golden else 2))
        current_health = int(
            (self.source.health - (self.source._health * (2 if self.source.golden else 1))) / (
                4 if self.source.golden else 2))

        new_buff = min(current_attack, current_health)

        self.source.player._spells_cast = min(current_buff, new_buff) if current_buff is not None else new_buff


class StormKingOnSummon(OnSummon):
    def handle(self, summoned_characters, stack, *args, **kwargs):
        if not self.source in summoned_characters:
            return

        spells_cast = self.source.player._spells_cast

        golden_multipler = 4 if self.source.golden else 2
        storm_king_buff = (spells_cast or 0) * golden_multipler

        Buff(reason=ActionReason.STORM_KING_BUFF, source=self.source, targets=[self.source],
             attack=storm_king_buff, health=storm_king_buff, temp=False).resolve()


class StormKingOnSpellCast(OnSpellCast):
    def handle(self, stack, *args, **kwargs):
        stat_buff = 4 if self.source.golden else 2

        Buff(reason=ActionReason.STORM_KING_BUFF, source=self.source, targets=[self.source],
             attack=stat_buff, health=stat_buff, temp=False, *args, **kwargs).resolve()


class CharacterType(Character):
    # TODO this needs to be changed after the resolve_board removal
    display_name = 'Scion of the Storm'

    _attack = 2
    _health = 2
    _level = 6
    _tribes = {Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.player.register(StormKingOnSpellCast, source=self)
        self.player.register(StormKingOnSummon, source=self, priority=-15)
        self.player.register(StormKingOnStart, source=self, priority=9000)

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
