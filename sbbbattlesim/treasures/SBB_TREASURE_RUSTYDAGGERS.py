from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Needle Nose Daggers'
    aura = True

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feather_used = False
        stats = 2 * (self.mimic + 1)
        self.aura_buff = Aura(reason=ActionReason.NEEDLE_NOSE_DAGGERS, source=self, attack=stats)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
