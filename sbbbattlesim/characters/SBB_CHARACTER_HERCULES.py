from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Hercules'
    quest = True

    _attack = 25
    _health = 25
    _level = 6
    _tribes = {Tribe.GOOD, Tribe.ROYAL}
    _quest_counter = 100
