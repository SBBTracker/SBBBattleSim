from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Pig'

    _attack = 10
    _health = 10
    _level = 1
    _tribes = {Tribe.ANIMAL,}