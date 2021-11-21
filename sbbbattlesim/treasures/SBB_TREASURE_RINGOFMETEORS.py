from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = '''Ring of Meteors'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class RingOfMeteorsActivation(OnStart):
            ring = self
            def handle(self, *args, **kwargs):
                for _ in range(self.ring.mimic + 1):
                    for char in self.manager.valid_characters() + self.manager.opponent.valid_characters():
                        char.change_stats(damage=1, reason=StatChangeCause.RING_OF_METEORS, source=self.ring)
                    self.manager.resolve_damage()

        self.player.register(RingOfMeteorsActivation)
