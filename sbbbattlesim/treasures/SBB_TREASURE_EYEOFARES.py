from sbbbattlesim.action import ActionReason, Aura
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Eye of Ares'
    aura = True

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attack = 5 * (self.mimic + 1)
        self.aura = Aura(reason=ActionReason.EYE_OF_ARES_BUFF, source=self, attack=attack,
                         _action=self.give_opponent_aura)

    def give_opponent_aura(self, _):
        if self.aura not in self.player.opponent.auras:
            self.player.opponent.auras.add(self.aura)
