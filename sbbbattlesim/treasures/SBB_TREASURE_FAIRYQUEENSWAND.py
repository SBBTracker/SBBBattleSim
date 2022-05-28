from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Fairy Queen\'s Wand'
    aura = True

    _level = 7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 5 * (bool(self.multiplier) + 1)
        self.aura = Aura(reason=ActionReason.FAIRY_QUEENS_WAND, source=self, health=stats, attack=stats)
