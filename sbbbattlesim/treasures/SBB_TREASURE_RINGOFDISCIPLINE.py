from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Six of Shields'
    aura = True

    _level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feather_used = False
        stats = 3 * (self.mimic + 1)
        self.aura_buff = Aura(reason=ActionReason.SIX_OF_SHIELDS, source=self, health=stats)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
