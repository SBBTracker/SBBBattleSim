from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Monkey\'s Paw'
    aura = True

    _level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = False

        class MonkeysPawOnStart(OnStart):
            monkey = self
            def handle(self, *args, **kwargs):
                self.monkey.active = len(self.monkey.player.valid_characters()) <= 6

        self.player.board.register(MonkeysPawOnStart)

    def buff(self, target_character, *args, **kwargs):
        if self.active:
            for _ in range(self.mimic + 1):
                target_character.change_stats(attack=6, health=6, reason=StatChangeCause.MONKEYS_PAW, source=self, temp=True, *args, **kwargs)
