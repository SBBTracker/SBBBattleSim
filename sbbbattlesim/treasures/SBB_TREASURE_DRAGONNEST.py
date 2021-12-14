from sbbbattlesim.action import Buff, AuraBuff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class TreasureType(Treasure):
    display_name = 'Dragon Nest'
    aura = True

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 5 * (self.mimic + 1)
        self.aura_buff = AuraBuff(reason=StatChangeCause.DRAGON_NEST, source=self, health=stats, attack=stats,
                                  _lambda=lambda char: Tribe.DRAGON in char.tribes)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
