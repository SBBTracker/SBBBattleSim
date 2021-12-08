from sbbbattlesim.action import Buff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Sword of Fire and Ice'
    aura = True

    _level = 5

    def buff(self, target_character, *args, **kwargs):
        if target_character.position <= 4:
            for _ in range(bool(self.mimic) + 1):
                Buff(reason=StatChangeCause.SWORD_OF_FIRE_AND_ICE, source=self, targets=[target_character],
                     health=6, temp=True, *args, **kwargs).resolve()
        else:
            for _ in range(bool(self.mimic) + 1):
                Buff(reason=StatChangeCause.SWORD_OF_FIRE_AND_ICE, source=self, targets=[target_character],
                     attack=6, temp=True, *args, **kwargs).resolve()
