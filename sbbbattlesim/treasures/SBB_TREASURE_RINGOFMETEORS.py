from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = '''Ring of Meteors'''

    def __init__(self, player):
        super().__init__(player)

        class RingOfMeteorsActivation(OnStart):
            def handle(self, *args, **kwargs):
                for char in player.valid_characters() + player.opponent.valid_characters():
                    char.change_stats(damage=1, reason=StatChangeCause.RING_OF_METEORS, source=self)

        self.player.register(RingOfMeteorsActivation)
