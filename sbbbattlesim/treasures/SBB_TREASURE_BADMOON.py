from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnSlay
from sbbbattlesim.treasures import Treasure


class BadMoonSlayBuff(OnSlay):
    def handle(self, source, stack, *args, **kwargs):
        for _ in range(self.source.multiplier + 1):
            Buff(reason=ActionReason.BAD_MOON, source=self.source, targets=[self.manager],
                 attack=1, health=2, stack=stack).resolve()


class TreasureType(Treasure):
    display_name = 'Bad Moon'
    aura = True

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(event=BadMoonSlayBuff, source=self)
