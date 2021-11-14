import collections

from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    # PUFF PUFF VARIABLE
    # Store the global Puff Puff buff
    # THIS IS WRONG
    display_name = 'PUFF PUFF'
    last_breath = True

    puffbuffs = collections.defaultdict(int)

    _attack = 7
    _health = 7
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.PUFF_PUFF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        current_buff = self.puffbuffs[self.owner.id]
        new_buff = min(self.attack, self.health) - (12 if self.golden else 6)
        self.puffbuffs[self.owner.id] = min(current_buff, new_buff) if current_buff != 0 else new_buff

        class PuffPuffDeath(OnDeath):
            last_breath = True

            def handle(self, *args, **kwargs):
                self.manager.change_stats(puffpuffbuff=2 if self.manager.golden else 1,
                                          reason=StatChangeCause.PUFF_PUFF_BUFF, source=self.manager)

        self.register(PuffPuffDeath)

    @property
    def attack(self):
        return super().attack + self.puffbuffs[self.owner.id]

    @property
    def health(self):
        return super().health + self.puffbuffs[self.owner.id]

    def change_stats(self, puffpuffbuff=0, *args, **kwargs):
        super().change_stats(*args, **kwargs)

        if puffpuffbuff > 0:
            self.puffbuffs[self.owner.id] += puffpuffbuff

            total_stat_change = len(self.owner.valid_characters(_lambda=lambda char: char.id == self.id)) * puffpuffbuff

            self('OnBuff', attack_buff=total_stat_change, health_buff=total_stat_change, reason=f'PuffPuffBuff', temp=False)
