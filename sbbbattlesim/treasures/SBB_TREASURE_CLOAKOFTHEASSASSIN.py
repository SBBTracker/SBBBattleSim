from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Cloak of the Assassin'

    def buff(self, target_character):
        if 'slay' in target_character.keywords:
            target_character.change_stats(health=3, attack=3, reason=StatChangeCause.CLOAK_OF_THE_ASSASSIN, source=self,
                                          temp=True)
