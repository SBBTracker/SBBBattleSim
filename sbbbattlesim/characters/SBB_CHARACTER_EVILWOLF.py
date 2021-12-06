from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Evil Sheep'

    _attack = 6
    _health = 6
    _level = 1
    _tribes = {Tribe.EVIL, Tribe.ANIMAL}