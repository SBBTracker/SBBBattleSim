from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnSetup
from sbbbattlesim.treasures import Treasure


class MonkeysPawOnSetup(OnSetup):
    def handle(self, *args, **kwargs):
        self.source.active = len(self.source.player.valid_characters()) <= 6


class TreasureType(Treasure):
    display_name = 'Monkey\'s Paw'
    aura = True

    _level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = False
        self.player.register(MonkeysPawOnSetup, source=self, priority=100)
        stats = 5 * (bool(self.mimic) + 1)
        self.aura = Aura(reason=ActionReason.MONKEYS_PAW, source=self, health=stats, attack=stats,
                         _lambda=lambda _: self.active)
