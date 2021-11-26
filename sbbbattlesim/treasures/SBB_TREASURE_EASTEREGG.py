from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Easter Egg'

    _level = 2

    def buff(self, target_character):
        if target_character.golden:
            target_character.change_stats(attack=3, health=3, reason=StatChangeCause.EASTER_EGG, source=self, temp=True)
