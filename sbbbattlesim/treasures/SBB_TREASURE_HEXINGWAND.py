from sbbbattlesim.action import Buff
from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


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

    def buff(self, target_character, *args, **kwargs):
        if self.active:
            for _ in range(self.mimic + 1):
                Buff(reason=StatChangeCause.MONKEYS_PAW, source=self, targets=[target_character],
                     attack=6, health=6, temp=True, *args, **kwargs).resolve()
