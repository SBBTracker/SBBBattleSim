from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Monkey\'s Paw'
    aura = True

    _level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monkey_paw = len(self.player.valid_characters()) <= 6

    def buff(self, target_character):
        if self.monkey_paw:
            for _ in range(self.mimic + 1):
                target_character.change_stats(attack=6, health=6, reason=StatChangeCause.MONKEYS_PAW, source=self, temp=True)
