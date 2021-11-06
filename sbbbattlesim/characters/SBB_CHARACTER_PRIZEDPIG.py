from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
import random


class CharacterType(Character):
    display_name = 'Prized Pig'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.PrizedPigLastBreath)

    class PrizedPigLastBreath(OnDeath):
        last_breath = True
        def handle(self, *args, **kwargs):
            pass  # this is only relevant for things like trophy hunter