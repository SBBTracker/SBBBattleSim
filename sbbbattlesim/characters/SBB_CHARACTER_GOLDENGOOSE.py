from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Greedy'

    _attack = 5
    _health = 9
    _level = 4
    _tribes = {Tribe.DWARF}
