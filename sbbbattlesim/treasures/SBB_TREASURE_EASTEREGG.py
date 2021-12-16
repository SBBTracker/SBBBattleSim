from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Easter Egg'

    aura = True

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 3 * (self.mimic + 1)
        self.aura_buff = Aura(reason=ActionReason.EASTER_EGG, source=self, health=stats, attack=stats,
                              _lambda=lambda char: char.golden)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
