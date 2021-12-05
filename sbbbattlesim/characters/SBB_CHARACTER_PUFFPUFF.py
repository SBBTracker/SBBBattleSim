import collections

from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath, OnSummon, OnStart
from sbbbattlesim.utils import StatChangeCause, Tribe
import logging

logger = logging.getLogger(__name__)

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

        class PuffPuffOnStart(OnStart):
            priority = 9000
            puff = self

            def handle(self, stack, *args, **kwargs):
                puffbuffs = self.puff.owner.stateful_effects['puffbuff']

                current_buff = puffbuffs[self.puff.owner.id]
                bonus_attack = int((self.puff.attack - self.puff._attack * (2 if self.puff.golden else 1)) / (2 if self.puff.golden else 1))
                bonus_health = int((self.puff.health - self.puff._health * (2 if self.puff.golden else 1)) / (2 if self.puff.golden else 1))

                new_buff = max(0, min(bonus_attack, bonus_health))

                if current_buff is None:
                    puffbuffs[self.puff.owner.id] = new_buff
                else:
                    puffbuffs[self.puff.owner.id] = min(current_buff, new_buff)


        class PuffPuffDeath(OnDeath):
            last_breath = True
            puff = self

            def handle(self, stack, *args, **kwargs):
                puffbuffs = self.puff.owner.stateful_effects['puffbuff']

                buff = 2 if self.puff.golden else 1
                for char in self.manager.owner.valid_characters(_lambda=lambda char: char.id == self.puff.id):
                    char.change_stats(attack=buff, health=buff, reason=StatChangeCause.PUFF_PUFF_BUFF,
                                      source=self.puff, stack=stack)

                if puffbuffs[self.puff.owner.id] is None:
                    puffbuffs[self.puff.owner.id] = 0
                puffbuffs[self.puff.owner.id] += buff

        class PuffPuffOnSummon(OnSummon):
            puff = self

            def handle(self, summoned_characters, stack, *args, **kwargs):
                if not self.puff in summoned_characters:
                    return

                puffbuffs = self.puff.owner.stateful_effects['puffbuff']

                golden_multipler = 2 if self.puff.golden else 1
                puff_buff = (puffbuffs[self.puff.owner.id] or 0) * golden_multipler

                self.puff.change_stats(attack=puff_buff, health=puff_buff, temp=False,
                                       reason=StatChangeCause.PUFF_PUFF_BUFF, source=self.puff)



        self.owner.register(PuffPuffOnSummon)
        self.register(PuffPuffDeath)
        self.owner.board.register(PuffPuffOnStart)

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
