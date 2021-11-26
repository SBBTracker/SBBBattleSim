from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Sheperd\'s Sling'
    aura = True

    _level = 3

    def buff(self, target_character):
        if target_character._level <= 3:
            for _ in range(self.mimic + 1):
                target_character.change_stats(health=1, attack=1, reason=StatChangeCause.SHEPHERDS_SLING, source=self, temp=True)
