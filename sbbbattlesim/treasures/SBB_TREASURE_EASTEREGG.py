from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Easter Egg'

    aura = True

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 3 * (self.multiplier + 1)
        self.aura = Aura(reason=ActionReason.EASTER_EGG, source=self, health=stats, attack=stats,
                         _lambda=lambda char: char.golden)
