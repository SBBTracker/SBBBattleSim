from sbbbattlesim.action import Buff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Sheperd\'s Sling'
    aura = True

    _level = 3

    def buff(self, target_character, *args, **kwargs):
        if target_character._level <= 3:
            for _ in range(self.mimic + 1):
                Buff(reason=StatChangeCause.SHEPHERDS_SLING, source=self, targets=[target_character],
                     health=1, attack=1, temp=True, *args, **kwargs).resolve()
