from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Moonsong Horn'
    aura = True

    _level = 4

    def buff(self, target_character):
        target_character.change_stats(health=1, attack=1, reason=StatChangeCause.MOONSONG_HORN_BUFF, source=self, temp=True)
        if self.mimic:
            target_character.change_stats(health=1, attack=1, reason=StatChangeCause.MOONSONG_HORN_BUFF, source=self, temp=True)

