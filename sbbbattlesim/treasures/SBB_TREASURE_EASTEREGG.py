from sbbbattlesim.action import Buff, AuraBuff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Easter Egg'

    aura = True

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 3 * (self.mimic + 1)
        self.aura_buff = AuraBuff(reason=StatChangeCause.EASTER_EGG, source=self, health=stats, attack=stats,
                                  _lambda=lambda char: char.golden)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
