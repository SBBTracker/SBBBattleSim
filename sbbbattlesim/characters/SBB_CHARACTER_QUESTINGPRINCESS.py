from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import Tribe


class BravePrincessSlay(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, *args, **kwargs):
        pass


class CharacterType(Character):
    display_name = 'Brave Princess'
    quest = True

    _attack = 5
    _health = 3
    _level = 3
    _tribes = {Tribe.GOOD, Tribe.ROYAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.golden:
            self.register(BravePrincessSlay)
