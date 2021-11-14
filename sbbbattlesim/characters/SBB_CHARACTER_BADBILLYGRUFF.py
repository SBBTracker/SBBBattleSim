from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'B-a-a-d Billy Gruff'

    _attack = 2
    _health = 3
    _level = 2
    _tribes = {Tribe.EVIL, Tribe.ANIMAL}
