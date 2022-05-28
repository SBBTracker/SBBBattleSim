from sbbbattlesim.action import Damage, ActionReason
from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure


class RingOfMeteorsActivation(OnStart):
    def handle(self, *args, **kwargs):
        for _ in range(self.source.mimic + 1):
            targets = self.source.player.valid_characters() + self.source.player.opponent.valid_characters()
            Damage(damage=1, reason=ActionReason.RING_OF_METEORS, source=self.source, targets=targets).resolve()


class TreasureType(Treasure):
    display_name = '''Ring of Meteors'''

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(event=RingOfMeteorsActivation, source=self, priority=-10)
