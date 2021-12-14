from sbbbattlesim.action import Buff, AuraBuff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Fountain Of Youth'
    aura = True

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 1 * (self.mimic + 1)
        self.aura_buff = AuraBuff(reason=StatChangeCause.FOUNTAIN_OF_YOUTH, source=self, health=stats)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
