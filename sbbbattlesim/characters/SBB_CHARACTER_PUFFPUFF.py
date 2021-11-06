import collections

from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath


class CharacterType(Character):
    # PUFF PUFF VARIABLE
    # Store the global Puff Puff buff
    # THIS IS WRONG
    display_name = 'PUFF PUFF'
    puffbuffs = collections.defaultdict(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        current_buff = self.puffbuffs[self.owner.id]
        new_buff = min(self.attack, self.health) - (12 if self.golden else 6)
        self.puffbuffs[self.owner.id] = min(current_buff, new_buff) if current_buff != 0 else new_buff

        class PuffPuffDeath(OnDeath):
            last_breath = True

            def handle(self, *args, **kwargs):
                self.manager.puffbuffs[self.manager.owner.id] += 2 if self.manager.golden else 1

        self.register(PuffPuffDeath)

    @property
    def attack(self):
        return super().attack + self.puffbuffs[self.owner.id]

    @property
    def health(self):
        return super().health + self.puffbuffs[self.owner.id]

    def change_stats(self, reason, puffpuffbuff=0, attack=0, health=0, damage=0, temp=True):
        super().change_stats(reason, attack, health, damage, temp)

        if puffpuffbuff > 0:
            self.puffbuffs[self.owner.id] += puffpuffbuff

            self('OnBuff', attack_buff=puffpuffbuff, health_buff=puffpuffbuff, reason=f'PuffPuffBuff', temp=False)
