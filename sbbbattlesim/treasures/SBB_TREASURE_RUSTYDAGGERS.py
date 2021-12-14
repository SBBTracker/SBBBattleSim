from sbbbattlesim.action import Buff, AuraBuff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Needle Nose Daggers'
    aura = True

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feather_used = False
        stats = 2 * (self.mimic + 1)
        self.aura_buff = AuraBuff(reason=StatChangeCause.NEEDLE_NOSE_DAGGERS, source=self, attack=stats)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
