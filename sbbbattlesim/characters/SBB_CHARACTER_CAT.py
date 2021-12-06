from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Cat'

    _attack = 1
    _health = 1
    _level = 1
    _tribes = {Tribe.EVIL, Tribe.ANIMAL}