from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import Tribe


class FeastingDragonSlay(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, *args, **kwargs):
        # TODO Summon random character or don't do this
        # TODO write any tests for this at all
        pass


class CharacterType(Character):
    display_name = 'Feasting Dragon'

    _attack = 5
    _health = 8
    _level = 4
    _tribes = {Tribe.DRAGON}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(FeastingDragonSlay)