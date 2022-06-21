import random

from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import Tribe


class PolyWoggleSlay(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, stack, *args, **kwargs):
        golden_promotion = (2 if self.source.golden else 1)
        _lambda = lambda char: char._level == min(self.manager.player.level + golden_promotion, 6)
        valid_chars = list(character_registry.filter(_lambda=_lambda))
        if valid_chars:
            char = random.choice(valid_chars)
            # TODO how to handle tribe complexity

            new_char = char(
                attack=char._attack + max(1, self.manager._base_attack - (2 if self.manager.golden else 1)),
                health=char._health + max(1, self.manager._base_health - (2 if self.manager.golden else 1)),
                golden=self.manager.golden,
                position=self.manager.position,
                player=self.manager.player,
                tribes=char._tribes,
                cost=char._level,
            )
            self.manager.player.transform(self.manager.position, new_char)


class CharacterType(Character):
    display_name = 'Polywoggle'

    _attack = 1
    _health = 1
    _level = 2
    _tribes = {Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(PolyWoggleSlay)
