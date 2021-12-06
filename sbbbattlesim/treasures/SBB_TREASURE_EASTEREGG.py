from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Easter Egg'

    aura = True

    _level = 2

    def buff(self, target_character, *args, **kwargs):
        if target_character.golden:
            for _ in range(self.mimic + 1):
                target_character.change_stats(attack=3, health=3, reason=StatChangeCause.EASTER_EGG, source=self, temp=True, *args, **kwargs)
