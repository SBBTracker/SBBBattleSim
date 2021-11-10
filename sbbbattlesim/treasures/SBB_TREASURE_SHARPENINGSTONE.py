from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Dancing Sword'

    def buff(self, target_character):
        target_character.change_stats(attack=1, reason=StatChangeCause.DANCING_SWORD, source=self, temp=True)
