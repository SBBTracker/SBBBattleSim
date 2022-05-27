from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Hercules'
    quest = True

    _attack = 20
    _health = 20
    _level = 6
    _tribes = {Tribe.GOOD, Tribe.ROYAL}
