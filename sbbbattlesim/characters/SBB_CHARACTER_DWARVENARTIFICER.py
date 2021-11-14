from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Crafy'

    _attack = 1
    _health = 1
    _level = 2
    _tribes = {Tribe.DWARF}
