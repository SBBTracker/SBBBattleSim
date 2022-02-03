from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Nutcracker'
    quest = True

    _attack = 4
    _health = 10
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.TREANT}
