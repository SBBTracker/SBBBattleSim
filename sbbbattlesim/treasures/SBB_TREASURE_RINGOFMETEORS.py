from sbbbattlesim.damage import Damage
from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class RingOfMeteorsActivation(OnStart):
    def handle(self, *args, **kwargs):
        for _ in range(self.ring.mimic + 1):
            targets = self.ring.player.valid_characters() + self.ring.player.opponent.valid_characters()
            Damage(1, reason=StatChangeCause.RING_OF_METEORS, source=self.ring, targets=targets).resolve()


class TreasureType(Treasure):
    display_name = '''Ring of Meteors'''

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.board.register(RingOfMeteorsActivation, ring=self)
