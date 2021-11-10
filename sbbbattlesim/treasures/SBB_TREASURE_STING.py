from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Sting'

    def buff(self, target_character):
        if 1 == target_character.position:
            target_character.change_stats(attack=10, reason=StatChangeCause.STING, source=self, temp=True)
