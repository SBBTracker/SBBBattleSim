from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Fountain Of Youth'
    aura = True

    _level = 2

    def buff(self, target_character, *args, **kwargs):
        for _ in range(self.mimic + 1):
            target_character.change_stats(health=1, reason=StatChangeCause.FOUNTAIN_OF_YOUTH, source=self, temp=True,
                                          *args, **kwargs)
