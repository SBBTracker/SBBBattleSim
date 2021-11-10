from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Tell Tale Quiver'

    def buff(self, target_character):
        if 5 <= target_character.position and 'ranged' in target_character.keywords:
            target_character.change_stats(health=3, attack=3, reason=StatChangeCause.TELL_TALE_QUIVER, source=self,
                                          temp=True)
