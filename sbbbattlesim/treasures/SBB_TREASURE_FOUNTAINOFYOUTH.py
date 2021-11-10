from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Fountain Of Youth'

    def buff(self, target_character):
        target_character.change_stats(health=1, reason=StatChangeCause.FOUNTAIN_OF_YOUTH, source=self, temp=True)
