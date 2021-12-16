from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Dancing Sword'
    aura = True

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 1 * (self.mimic + 1)
        self.aura_buff = Aura(reason=ActionReason.DANCING_SWORD, source=self, attack=stats)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
