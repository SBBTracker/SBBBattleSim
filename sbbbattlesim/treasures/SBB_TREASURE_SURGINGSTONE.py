from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Ring of Rage'
    aura = True

    _level = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 3 * (self.mimic + 1)
        self.aura_buff = Aura(reason=ActionReason.RING_OF_RAGE, source=self, attack=stats,
                              _lambda=lambda char: char.position == 1)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
