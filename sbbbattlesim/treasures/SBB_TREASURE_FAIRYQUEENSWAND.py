from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Fairy Queen\'s Wand'

    def buff(self, target_character):
        target_character.change_stats(health=5, attack=5, reason=StatChangeCause.FAIRY_QUEENS_WAND, source=self,
                                      temp=True)
