from sbbbattlesim.action import Buff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Fairy Queen\'s Wand'
    aura = True

    _level = 7

    def buff(self, target_character, *args, **kwargs):
        for _ in range(bool(self.mimic) + 1):
            Buff(reason=StatChangeCause.FAIRY_QUEENS_WAND, source=self, targets=[target_character],
                 health=5, attack=5, temp=True, *args, **kwargs).resolve()
