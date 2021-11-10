from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Sword of Fire and Ice'

    def buff(self, target_character):
        if 4 <= target_character.position:
            target_character.change_stats(health=5, reason=StatChangeCause.SWORD_OF_FIRE_AND_ICE, source=self,
                                          temp=True)
        else:
            target_character.change_stats(attack=5, reason=StatChangeCause.SWORD_OF_FIRE_AND_ICE, source=self,
                                          temp=True)
