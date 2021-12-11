from sbbbattlesim.action import Buff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Noble Steed'
    aura = True

    _level = 2

    def buff(self, target_character, *args, **kwargs):
        if target_character.quest:
            for _ in range(self.mimic + 1):
                Buff(reason=StatChangeCause.NOBLE_STEED, source=self, targets=[target_character],
                     health=1, attack=1, temp=True, *args, **kwargs).resolve()
