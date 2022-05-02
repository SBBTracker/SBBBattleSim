from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Sleeping Princess'

    _attack = 0
    _health = 8
    _level = 3
    _tribes = {Tribe.GOOD, Tribe.ROYAL}
