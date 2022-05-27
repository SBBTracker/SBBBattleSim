import collections

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath, OnSummon, OnStart
from sbbbattlesim.utils import Tribe
import logging

logger = logging.getLogger(__name__)


class PuffPuffOnStart(OnStart):
    def handle(self, stack, *args, **kwargs):
        puffbuffs = self.source.player.stateful_effects.setdefault('puffbuff', collections.defaultdict())

        current_buff = puffbuffs.get(self.source.player.id)
        golden_multiplier = 2 if self.source.golden else 1
        bonus_attack = int((self.source.attack - self.source._attack * golden_multiplier) / golden_multiplier)
        bonus_health = int((self.source.health - self.source._health * golden_multiplier) / golden_multiplier)

        new_buff = max(0, min(bonus_attack, bonus_health))

        if current_buff is None:
            puffbuffs[self.source.player.id] = new_buff
        else:
            puffbuffs[self.source.player.id] = min(current_buff, new_buff)


class PuffPuffDeath(OnDeath):
    last_breath = True

    def handle(self, stack, *args, **kwargs):
        puffbuffs = self.source.player.stateful_effects.setdefault('puffbuff', collections.defaultdict())

        buff = 2 if self.source.golden else 1
        puffpuffs = self.manager.player.valid_characters(_lambda=lambda char: char.id == self.source.id)
        Buff(reason=ActionReason.PUFF_PUFF_BUFF, source=self.source, attack=buff, health=buff, stack=stack).execute(*puffpuffs)

        # in case of random summon
        if not self.source.player.id in puffbuffs:
            puffbuffs[self.source.player.id] = None

        if puffbuffs[self.source.player.id] is None:
            puffbuffs[self.source.player.id] = 0
        puffbuffs[self.source.player.id] += buff


class PuffPuffOnSummon(OnSummon):
    def handle(self, summoned_characters, stack, *args, **kwargs):
        if not self.source in summoned_characters:
            return

        puffbuffs = self.source.player.stateful_effects.setdefault('puffbuff', collections.defaultdict())

        golden_multipler = 2 if self.source.golden else 1
        puff_buff = (puffbuffs.get(self.source.player.id) or 0) * golden_multipler
        Buff(attack=puff_buff, health=puff_buff, temp=False,
             reason=ActionReason.PUFF_PUFF_BUFF, source=self.source,
             targets=[self.source]).resolve()


class CharacterType(Character):
    display_name = 'PUFF PUFF'
    last_breath = True

    _attack = 7
    _health = 7
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.PUFF_PUFF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.player.register(PuffPuffOnSummon, source=self, priority=-15)
        self.register(PuffPuffDeath)
        self.player.register(PuffPuffOnStart, source=self, priority=9000)

    @classmethod
    def new(cls, *args, **kwargs):
        self = super().new(*args, **kwargs)

        # TODO this logic will come back in the future
        # self.player.resolve_board()
        #
        # stat_buff = (self.player.stateful_effects['puffbuffs'][self.player.id] or 0)
        #
        # self.change_stats(
        #     attack=stat_buff,
        #     health=stat_buff,
        #     reason=StatChangeCause.PUFF_PUFF_BUFF,
        #     source=self,
        # )

        return self
