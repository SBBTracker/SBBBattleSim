from sbbbattlesim.action import Buff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Easter Egg'

    aura = True

    _level = 2

    def buff(self, target_character, *args, **kwargs):
        if target_character.golden:
            for _ in range(self.mimic + 1):
                Buff(reason=StatChangeCause.EASTER_EGG, source=self, targets=[target_character],
                     attack=3, health=3,  temp=True, *args, **kwargs).resolve()
