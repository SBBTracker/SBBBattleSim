from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Keyword


class TreasureType(Treasure):
    display_name = 'Noble Steed'

    def buff(self, target_character):
        if Keyword.QUEST in target_character.keywords:
            target_character.change_stats(health=1, attack=1, reason=StatChangeCause.NOBLE_STEED, source=self,
                                          temp=True)
