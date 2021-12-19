from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Mama Bear'

    _attack = 4
    _health = 4
    _level = 1
    _tribes = {Tribe.GOOD, Tribe.ANIMAL}
