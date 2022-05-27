from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Awoken Princess'

    _attack = 8
    _health = 8
    _level = 3
    _tribes = {Tribe.GOOD, Tribe.ROYAL}
