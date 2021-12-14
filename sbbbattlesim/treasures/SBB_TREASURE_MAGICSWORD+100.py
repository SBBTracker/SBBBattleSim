from sbbbattlesim.action import Buff, AuraBuff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Magic Sword +100'
    aura = True

    _level = 7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 100 * (bool(self.mimic) + 1)
        self.aura_buff = AuraBuff(reason=StatChangeCause.MAGIC_SWORD, source=self, attack=stats,
                                  _lambda=lambda char: char.position == 1)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
