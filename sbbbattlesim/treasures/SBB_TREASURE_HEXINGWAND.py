from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure


class MonkeysPawOnStart(OnStart):
    def handle(self, *args, **kwargs):
        self.monkey.active = len(self.monkey.player.valid_characters()) <= 6


class TreasureType(Treasure):
    display_name = 'Monkey\'s Paw'
    aura = True

    _level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = False
        self.player.board.register(MonkeysPawOnStart, monkey=self)
        stats = 6 * (bool(self.mimic) + 1)
        self.aura_buff = Aura(reason=ActionReason.MONKEYS_PAW, source=self, health=stats, attack=stats,
                              _lambda=lambda _: self.active)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
