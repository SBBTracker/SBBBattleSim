from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Six of Shields'

    def buff(self, target_character):
        target_character.change_stats(health=3, reason=StatChangeCause.SIX_OF_SHIELDS, source=self, temp=True)
