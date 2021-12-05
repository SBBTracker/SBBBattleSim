from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Nian, Sea Terror'

    _attack = 10
    _health = 10
    _level = 5
    _tribes = {Tribe.EVIL, Tribe.MONSTER}
