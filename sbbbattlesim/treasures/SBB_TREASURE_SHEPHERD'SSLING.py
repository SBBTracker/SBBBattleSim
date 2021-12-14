from sbbbattlesim.action import Buff, AuraBuff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Sheperd\'s Sling'
    aura = True

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feather_used = False
        stats = 1 * (self.mimic + 1)
        self.aura_buff = AuraBuff(reason=StatChangeCause.NEEDLE_NOSE_DAGGERS, source=self, attack=stats, health=stats,
                                  _lambda=lambda char: char._level <= 3)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
