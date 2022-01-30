from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Sword of Fire and Ice'
    aura = True

    _level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 6 * (bool(self.mimic) + 1)
        self.aura = {
            Aura(reason=ActionReason.SWORD_OF_FIRE_AND_ICE, source=self, health=stats,
                 _lambda=lambda char: char.position <= 4),
            Aura(reason=ActionReason.SWORD_OF_FIRE_AND_ICE, source=self, attack=stats,
                 _lambda=lambda char: char.position > 4),
        }
