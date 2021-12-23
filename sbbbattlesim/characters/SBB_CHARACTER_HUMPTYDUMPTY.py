from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe
from sbbbattlesim.events import OnDeath


class HumptyDumptyOnDeath(OnDeath):
    last_breath = False

    def handle(self, stack, reason, *args, **kwargs):
        self.manager.player.graveyard.remove(self.source)


class CharacterType(Character):
    display_name = 'Humpty Dumpty'

    _attack = 7
    _health = 7
    _level = 2
    _tribes = {Tribe.GOOD, Tribe.EGG}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(HumptyDumptyOnDeath, priority=1001)
