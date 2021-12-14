from sbbbattlesim.action import Buff, AuraBuff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class TreasureType(Treasure):
    display_name = 'Sky Castle'
    aura = True

    _level = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feather_used = False
        stats = 4 * (bool(self.mimic) + 1)
        self.aura_buff = AuraBuff(reason=StatChangeCause.SKYCASTLE, source=self, attack=stats, health=stats,
                                  _lambda=lambda char: Tribe.PRINCE in char.tribes or Tribe.PRINCESS in char.tribes)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
