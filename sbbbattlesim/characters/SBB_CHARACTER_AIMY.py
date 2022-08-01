from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Amy'
    ranged = True

    _attack = 6
    _health = 6
    _level = 4
    _tribes = {Tribe.DWARF}
