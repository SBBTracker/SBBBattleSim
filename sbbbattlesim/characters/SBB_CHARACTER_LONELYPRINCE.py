from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Lonely Prince'

    _attack = 1
    _health = 1
    _level = 2
    _tribes = {Tribe.GOOD, Tribe.ROYAL}
