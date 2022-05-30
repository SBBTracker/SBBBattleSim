from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Sheperd\'s Sling'
    aura = True

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 1 * (self.multiplier + 1)
        self.aura = Aura(reason=ActionReason.NEEDLE_NOSE_DAGGERS, source=self, attack=stats, health=stats,
                         _lambda=lambda char: char._level <= 3)
