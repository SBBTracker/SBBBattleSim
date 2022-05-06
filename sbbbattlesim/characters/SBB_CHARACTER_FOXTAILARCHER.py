from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Sherwood Sureshot'
    ranged = True

    _attack = 2
    _health = 1
    _level = 2
    _tribes = {Tribe.GOOD, Tribe.ROYAL}
