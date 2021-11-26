from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Dancing Sword'
    aura = True

    _level = 2

    def buff(self, target_character):
        for _ in range(self.mimic + 1):
            target_character.change_stats(attack=1, reason=StatChangeCause.DANCING_SWORD, source=self, temp=True)
