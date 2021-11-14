from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Happy Little Tree'

    _attack = 1
    _health = 1
    _level = 2
    _tribes = {Tribe.GOOD, Tribe.TREANT}
