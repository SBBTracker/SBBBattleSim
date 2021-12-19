from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Big Pig'

    _attack = 5
    _health = 5
    _level = 1
    _tribes = {Tribe.EVIL, Tribe.ANIMAL}
