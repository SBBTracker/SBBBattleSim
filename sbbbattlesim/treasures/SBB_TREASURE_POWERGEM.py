from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Moonsong Horn'
    aura = True

    _level = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 1 * (self.multiplier + 1)
        self.aura = Aura(reason=ActionReason.MOONSONG_HORN_BUFF, source=self, health=stats, attack=stats)
