from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Tweedle Dum'

    _attack = 0
    _health = 0
    _level = 1
    _tribes = {Tribe.DWARF}
