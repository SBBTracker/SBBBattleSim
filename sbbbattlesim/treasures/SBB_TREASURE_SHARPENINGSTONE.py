from sbbbattlesim.utils import Tribe

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Dancing Sword'
    aura = True

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 1 * (self.mimic + 1)
        self.aura = Aura(reason=ActionReason.DANCING_SWORD, source=self, _lambda=lambda char: Tribe.EVIL in char.tribes,
                         attack=stats, health=stats)
