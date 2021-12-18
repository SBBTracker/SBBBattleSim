from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import Tribe


class TreasureType(Treasure):
    display_name = 'Sky Castle'
    aura = True

    _level = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feather_used = False
        stats = 4 * (bool(self.mimic) + 1)
        self.aura = Aura(reason=ActionReason.SKYCASTLE, source=self, attack=stats, health=stats,
                              _lambda=lambda char: Tribe.PRINCE in char.tribes or Tribe.PRINCESS in char.tribes)

    
