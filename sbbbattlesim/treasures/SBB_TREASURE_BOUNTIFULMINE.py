from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class TreasureType(Treasure):
    display_name = 'Deepstone Mine'

    def buff(self, target_character):
        if Tribe.DWARF in target_character.tribes:
            target_character.change_stats(attack=2, health=2, reason=StatChangeCause.DEEPSTONE_MINE, source=self,
                                          temp=True)