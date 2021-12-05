from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Blind Mouse'

    _attack = 2
    _health = 2
    _level = 2
    _tribes = {Tribe.ANIMAL}
