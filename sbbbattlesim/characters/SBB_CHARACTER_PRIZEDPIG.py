from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath

from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Prized Pig'
    last_breath = True

    _attack = 3
    _health = 6
    _level = 3
    _tribes = {Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.PrizedPigLastBreath)

    class PrizedPigLastBreath(OnDeath):
        last_breath = True
        def handle(self, *args, **kwargs):
            pass  # this is only relevant for things like trophy hunter