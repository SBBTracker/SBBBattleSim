from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Time Flies'

    _attack = 3
    _health = 3
    _level = 5
    _tribes = {Tribe.ANIMAL}