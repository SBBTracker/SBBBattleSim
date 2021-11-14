from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Polywoggle'
    slay = True

    _attack = 1
    _health = 1
    _level = 2
    _tribes = {Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.PolywoggleSlay)

    class PolywoggleSlay(OnAttackAndKill):
        slay = True
        def handle(self, killed_character, *args, **kwargs):
            pass  #TODO implement random spawn on survive
