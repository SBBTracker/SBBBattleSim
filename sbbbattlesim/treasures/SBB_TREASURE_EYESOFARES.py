from sbbbattlesim.action import ActionReason, Aura
from sbbbattlesim.events import OnSetup
from sbbbattlesim.treasures import Treasure


class EyeOfAresOnSetup(OnSetup):
    def handle(self, stack, *args, **kwargs):
        self.source.player.opponent.auras.add(self.source.aura)


class TreasureType(Treasure):
    display_name = 'Eye of Ares'
    aura = True

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attack = 5 * (self.mimic + 1)
        self.aura = Aura(reason=ActionReason.EYE_OF_ARES_BUFF, source=self, attack=attack)
        self.player.register(EyeOfAresOnSetup, priority=100, source=self)

