from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Magic Sword +100'
    aura = True

    _level = 7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 100 * (bool(self.multiplier) + 1)
        self.aura = Aura(reason=ActionReason.MAGIC_SWORD, source=self, attack=stats,
                         _lambda=lambda char: char.position == 1)
