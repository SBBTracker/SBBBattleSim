from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import Tribe


class OgrePrincessSlay(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, *args, **kwargs):
        # TODO Summon random character or don't do this
        # TODO write any tests for this at all
        pass


class CharacterType(Character):
    display_name = 'Orge Princess'

    _attack = 4
    _health = 2
    _level = 3
    _tribes = {Tribe.GOOD, Tribe.ROYAL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(OgrePrincessSlay)
