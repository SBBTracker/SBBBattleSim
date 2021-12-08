from sbbbattlesim.action import Buff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Needle Nose Daggers'
    aura = True

    _level = 2

    def buff(self, target_character, *args, **kwargs):
        for _ in range(self.mimic + 1):
            Buff(reason=StatChangeCause.NEEDLE_NOSE_DAGGERS, source=self, targets=[target_character],
                 attack=2, temp=True, *args, **kwargs).resolve()
