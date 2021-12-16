import logging

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure

logger = logging.getLogger(__name__)


class CoinOfCharonOnDeath(OnDeath):
    last_breath = False

    def handle(self, stack, *args, **kwargs):
        if self.manager._level < 2:
            return

        # This should only proc once per combat
        if self.coin.coin_trigger:
            return  # This has already procced
        self.coin.coin_trigger = True

        for _ in range(self.coin.mimic + 1):
            Buff(reason=ActionReason.COIN_OF_CHARON, source=self.coin, targets=[self.manager],
                 attack=4, health=4, stack=stack).execute()


class TreasureType(Treasure):
    name = 'Coin of Charon'
    aura = True

    _level = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.coin_trigger = False
        self.aura_buff = Aura(event=CoinOfCharonOnDeath, source=self, priority=400, coin=self)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
