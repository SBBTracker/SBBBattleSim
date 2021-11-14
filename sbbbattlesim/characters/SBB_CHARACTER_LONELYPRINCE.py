from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Lonely Prince'

    _attack = 5
    _health = 5
    _level = 2
    _tribes = {Tribe.GOOD, Tribe.PRINCE}
