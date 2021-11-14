from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Great Pumpkin King'

    _attack = 5
    _health = 5
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.MONSTER}
