from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Frog Prince'

    _attack = 5
    _health = 5
    _level = 2
    _tribes = {Tribe.GOOD, Tribe.ROYAL}
