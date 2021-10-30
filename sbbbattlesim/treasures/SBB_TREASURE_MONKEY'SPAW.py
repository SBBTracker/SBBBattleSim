from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath
import random
import logging

logger = logging.getLogger(__name__)

COIN_OF_CHARON_STR = 'CoinOfCharon_Proc'

class CoinOfCharonOnDeath(OnDeath):
    priority = 999
    def handle(self, *args, **kwargs):
        itr = 1 # TODO this may be useful when dealing with mimic

        # This should only proc once per combat
        if self.manager.owner.stateful_effects.get(COIN_OF_CHARON_STR, False):
           return  # This has already procced
        self.manager.owner.stateful_effects[COIN_OF_CHARON_STR] = True

        for _ in range(itr):
            self.manager.base_health += 4
            self.manager.base_attack += 4

class TreasureType(Treasure):
    name = 'Coin of Charon'
    aura = True

    def buff(self, target_character):
        target_character.register(CoinOfCharonOnDeath, temp=True)

