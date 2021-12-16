from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Noble Steed'
    aura = True

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feather_used = False
        stats = 1 * (self.mimic + 1)
        self.aura_buff = Aura(reason=ActionReason.NOBLE_STEED, source=self, health=stats, attack=stats,
                              _lambda=lambda char: char.quest)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
