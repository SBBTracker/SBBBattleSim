from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class TreasureType(Treasure):
    display_name = 'Sky Castle'

    def buff(self, target_character):
        if Tribe.PRINCE in target_character.tribes or Tribe.PRINCESS in target_character.tribes:
            target_character.change_stats(health=4, attack=4, reason=StatChangeCause.SKYCASTLE, source=self, temp=True)
