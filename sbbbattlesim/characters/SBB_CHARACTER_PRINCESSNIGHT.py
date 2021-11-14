from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Princess Wight'

    _attack = 2
    _health = 4
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.PRINCESS}
