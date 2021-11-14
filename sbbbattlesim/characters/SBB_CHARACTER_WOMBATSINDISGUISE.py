from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Tiny'

    _attack = 4
    _health = 4
    _level = 5
    _tribes = {Tribe.ANIMAL}
