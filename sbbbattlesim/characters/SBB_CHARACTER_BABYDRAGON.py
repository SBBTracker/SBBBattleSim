from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Baby Dragon'
    flying = True

    _attack = 3
    _health = 2
    _level = 2
    _tribes = {Tribe.DRAGON, }
