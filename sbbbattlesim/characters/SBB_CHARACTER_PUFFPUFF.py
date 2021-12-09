import collections

from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath, OnSummon, OnStart
from sbbbattlesim.utils import StatChangeCause, Tribe
import logging

logger = logging.getLogger(__name__)


class PuffPuffOnStart(OnStart):
    def handle(self, stack, *args, **kwargs):
        puffbuffs = self.puff.owner.stateful_effects.setdefault('puffbuff', collections.defaultdict())

        current_buff = puffbuffs.get(self.puff.owner.id)
        golden_multiplier = 2 if self.puff.golden else 1
        bonus_attack = int((self.puff.attack - self.puff._attack * golden_multiplier) / golden_multiplier)
        bonus_health = int((self.puff.health - self.puff._health * golden_multiplier) / golden_multiplier)

        new_buff = max(0, min(bonus_attack, bonus_health))

        if current_buff is None:
            puffbuffs[self.puff.owner.id] = new_buff
        else:
            puffbuffs[self.puff.owner.id] = min(current_buff, new_buff)


class PuffPuffDeath(OnDeath):
    last_breath = True

    def handle(self, stack, *args, **kwargs):
        puffbuffs = self.puff.owner.stateful_effects.setdefault('puffbuff', collections.defaultdict())

        buff = 2 if self.puff.golden else 1
        puffpuffs = self.manager.owner.valid_characters(_lambda=lambda char: char.id == self.puff.id)
        Buff(reason=StatChangeCause.PUFF_PUFF_BUFF, source=self.puff, targets=puffpuffs,
             attack=buff, health=buff, stack=stack).execute()

        if puffbuffs[self.puff.owner.id] is None:
            puffbuffs[self.puff.owner.id] = 0
        puffbuffs[self.puff.owner.id] += buff


class PuffPuffOnSummon(OnSummon):
    def handle(self, summoned_characters, stack, *args, **kwargs):
        if not self.puff in summoned_characters:
            return

        puffbuffs = self.puff.owner.stateful_effects.setdefault('puffbuff', collections.defaultdict())

        golden_multipler = 2 if self.puff.golden else 1
        puff_buff = (puffbuffs.get(self.puff.owner.id) or 0) * golden_multipler
        Buff(attack=puff_buff, health=puff_buff, temp=False,
             reason=StatChangeCause.PUFF_PUFF_BUFF, source=self.puff,
             targets=[self.puff]).resolve()


class CharacterType(Character):
    # TODO this will need to be revisited after the resolve board removal

    display_name = 'PUFF PUFF'
    last_breath = True

    _attack = 7
    _health = 7
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.PUFF_PUFF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.owner.register(PuffPuffOnSummon, puff=self, priority=-15)
        self.register(PuffPuffDeath, puff=self)
        self.owner.board.register(PuffPuffOnStart, puff=self, priority=9000)

    @classmethod
    def new(cls, *args, **kwargs):
        self = super().new(*args, **kwargs)

        # TODO this logic will come back in the future
        # self.owner.resolve_board()
        #
        # stat_buff = (self.owner.stateful_effects['puffbuffs'][self.owner.id] or 0)
        #
        # self.change_stats(
        #     attack=stat_buff,
        #     health=stat_buff,
        #     reason=StatChangeCause.PUFF_PUFF_BUFF,
        #     source=self,
        # )

        return self
