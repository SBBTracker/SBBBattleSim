from numpy import character

from sbbbattlesim.action import Buff, AuraBuff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Sword of Fire and Ice'
    aura = True

    _level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 6 * (bool(self.mimic) + 1)
        self.aura_buff = {
            AuraBuff(reason=StatChangeCause.SWORD_OF_FIRE_AND_ICE, source=self, health=stats,
                     _lambda=lambda char: char.position <= 4),
            AuraBuff(reason=StatChangeCause.SWORD_OF_FIRE_AND_ICE, source=self, attack=stats,
                     _lambda=lambda char: char.position > 4),
        }

    def buff(self, target_character, *args, **kwargs):
        for aura in self.aura_buff:
            aura.execute(target_character)
