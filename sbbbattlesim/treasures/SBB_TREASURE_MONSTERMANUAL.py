from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import Tribe


class MonsterManualOnDeath(OnDeath):
    last_breath = False

    def handle(self, stack, *args, **kwargs):
        for _ in range(self.manual.mimic + 1):
            Buff(reason=ActionReason.MONSTER_MANUAL_BUFF, source=self.manual, targets=[self.manager],
                 attack=2, stack=stack).execute()


class TreasureType(Treasure):
    display_name = 'Monster Manual'
    aura = True

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.coin_trigger = False
        self.aura = Aura(event=MonsterManualOnDeath, source=self, manual=self, priority=400,
                                   _lambda=lambda char: Tribe.MONSTER in char.tribes)

    
