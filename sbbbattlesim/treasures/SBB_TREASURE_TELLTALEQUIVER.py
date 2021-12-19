from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Tell Tale Quiver'
    aura = True

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 3 * (self.mimic + 1)
        self.aura = Aura(reason=ActionReason.TELL_TALE_QUIVER, source=self, health=stats, attack=stats,
                         _lambda=lambda char: char.position >= 5 and char.ranged)
