import random

from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Polywoggle'

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
                if valid_chars:
                    char = random.choice(valid_chars)
                    # TODO how to handle tribe complexity

                    new_char = char(
                        attack=char._attack + self.manager._base_attack - (2 if self.manager.golden else 1),
                        health=char._health + self.manager._base_health - (2 if self.manager.golden else 1),
                        golden=self.manager.golden,
                        position=self.manager.position,
                        owner=self.manager.owner,
                        tribes=char._tribes,
                        cost=char._level,
                    )
                    self.manager.owner.characters[self.manager.position] = new_char
                    self.manager.position = 'polywoggle-land'

                    self.manager.owner._attack_slot += 1
                    if self.manager.owner._attack_slot > 7:
                        self.manager.owner._attack_slot = 1

        self.register(PolywoggleSlay)

