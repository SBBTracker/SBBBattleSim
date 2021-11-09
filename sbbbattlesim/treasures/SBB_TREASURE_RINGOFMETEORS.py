import random

from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = '''Ring of Meteors'''

    def __init__(self, player):
        super().__init__(player)

        class RingOfMeteorsActivation(OnStart):
            def handle(self, *args, **kwargs):
                for char in player.valid_characters() + player.opponent.valid_characters():
                    char.change_stats(damage=1, reason=221, source=self)

        self.player.register(RingOfMeteorsActivation)
