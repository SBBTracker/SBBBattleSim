from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Monkey\'s Paw'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monkey_paw = len(self.player.valid_characters()) <= 6

    def buff(self, target_character):
        if self.monkey_paw:
            target_character.change_stats(attack=6, health=6, reason=StatChangeCause.MONKEYS_PAW, source=self, temp=True)
