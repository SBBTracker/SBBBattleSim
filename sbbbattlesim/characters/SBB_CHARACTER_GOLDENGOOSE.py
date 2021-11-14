from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Greedy'

    _attack = 4
    _health = 8
    _level = 4
    _tribes = {Tribe.DWARF}
