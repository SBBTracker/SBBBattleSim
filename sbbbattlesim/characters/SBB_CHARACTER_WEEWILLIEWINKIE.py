from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Tiny'

    _attack = 6
    _health = 1
    _level = 2
    _tribes = {Tribe.DWARF}
