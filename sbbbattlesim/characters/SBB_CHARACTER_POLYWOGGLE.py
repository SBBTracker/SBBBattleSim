from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import Tribe
from sbbbattlesim.characters import registry as character_registry
import random

class CharacterType(Character):
    display_name = 'Polywoggle'
    slay = True

    _attack = 1
    _health = 1
    _level = 2
    _tribes = {Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class PolywoggleSlay(OnAttackAndKill):
            slay = True
            woggle = self

            def handle(self, killed_character, *args, **kwargs):
                _lambda = lambda char: char._level == min(self.manager.owner.level + 1, 6)
                valid_chars = list(character_registry.filter(_lambda=_lambda))

                char = random.choice(valid_chars)
                # TODO lmao who knows

        self.register(PolywoggleSlay)

