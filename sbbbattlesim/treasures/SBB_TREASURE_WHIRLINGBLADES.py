from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Singing Swords'
    aura = True

    _level = 6

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 15 * (self.mimic + 1)
        self.aura = Aura(reason=ActionReason.SINGINGSWORD_BUFF, source=self, attack=stats,
                         _lambda = lambda char: char.position in [1, 2, 3, 4] )
