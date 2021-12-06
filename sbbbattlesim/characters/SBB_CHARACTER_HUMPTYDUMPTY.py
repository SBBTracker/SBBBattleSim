from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe
from sbbbattlesim.events import OnDeath


class CharacterType(Character):
    display_name = 'Humpty Dumpty'

    _attack = 7
    _health = 7
    _level = 2
    _tribes = {Tribe.GOOD, Tribe.EGG}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class HumptyDumptyOnDeath(OnDeath):
            last_breath = False
            egg = self
            priority = 1001

            def handle(self, *args, **kwargs):
                self.manager.owner.graveyard.remove(self.egg)

        self.register(HumptyDumptyOnDeath)
