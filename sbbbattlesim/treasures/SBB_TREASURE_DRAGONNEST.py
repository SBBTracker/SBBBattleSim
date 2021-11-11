from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class TreasureType(Treasure):
    display_name = 'Dragon Nest'

    def buff(self, target_character):
        if Tribe.DRAGON in target_character.tribes:
            target_character.change_stats(attack=5, health=5, reason=StatChangeCause.DRAGON_NEST, source=self,
                                          temp=True)
