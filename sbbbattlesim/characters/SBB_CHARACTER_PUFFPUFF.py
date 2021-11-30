import collections

from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    # PUFF PUFF VARIABLE
    # Store the global Puff Puff buff
    # THIS IS WRONG
    # TODO This is broken
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
            puff = self

            def handle(self, stack, *args, **kwargs):
                for char in self.manager.owner.valid_characters(_lambda=lambda char: char.id == self.puff.id):
                    buff = 4 if self.puff.golden else 2
                    char.change_stats(attack=buff, health=buff, reason=StatChangeCause.PUFF_PUFF_BUFF,
                                      source=self.puff, stack=stack)
                    self.puff.puffbuffs[self.puff.owner.id] += buff

        self.register(PuffPuffDeath)

