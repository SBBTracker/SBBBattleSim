from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Fairy Queen\'s Wand'
    aura = True

    _level = 7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 5 * (bool(self.mimic) + 1)
        self.aura_buff = Aura(reason=ActionReason.FAIRY_QUEENS_WAND, source=self, health=stats, attack=stats)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
