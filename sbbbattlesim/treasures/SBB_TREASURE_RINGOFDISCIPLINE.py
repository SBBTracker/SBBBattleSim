from sbbbattlesim.action import Buff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Six of Shields'
    aura = True

    _level = 5

    def buff(self, target_character, *args, **kwargs):
        for _ in range(self.mimic + 1):
            Buff(reason=StatChangeCause.SIX_OF_SHIELDS, source=self, targets=[target_character],
                 health=3,  temp=True, *args, **kwargs).resolve()
