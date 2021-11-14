from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Golden Chicken'

    _attack = 2
    _health = 2
    _level = 2
    _tribes = {Tribe.ANIMAL}
