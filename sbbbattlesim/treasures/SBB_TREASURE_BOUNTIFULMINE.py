from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import Tribe


class TreasureType(Treasure):
    display_name = 'Deepstone Mine'
    aura = True

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 2 * (self.mimic + 1)
        self.aura_buff = Aura(reason=ActionReason.DEEPSTONE_MINE, source=self, attack=stats, health=stats,
                              _lambda=lambda char: Tribe.DWARF in char.tribes)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
