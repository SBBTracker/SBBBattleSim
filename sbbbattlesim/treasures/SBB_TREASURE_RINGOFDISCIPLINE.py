from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Six of Shields'
    aura = True

    _level = 5

    def buff(self, target_character, *args, **kwargs):
        for _ in range(self.mimic + 1):
            target_character.change_stats(health=3, reason=StatChangeCause.SIX_OF_SHIELDS, source=self, temp=True, *args, **kwargs)
