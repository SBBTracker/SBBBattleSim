from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath

from sbbbattlesim.utils import Tribe


class LuckyLastBreath(OnDeath):
    last_breath = True

    def handle(self, stack, reason, *args, **kwargs):
        pass  # this is only relevant for things like trophy hunter


class CharacterType(Character):
    display_name = 'Lucky'
    last_breath = True

    _attack = 3
    _health = 2
    _level = 3
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(LuckyLastBreath)
