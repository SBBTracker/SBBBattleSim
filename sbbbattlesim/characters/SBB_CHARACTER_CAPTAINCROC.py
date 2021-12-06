from sbbbattlesim.characters import Character
from sbbbattlesim.exceptions import SBBBSCrocException
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Captain Croc'
    last_breath = True

    _attack = 10
    _health = 10
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        raise SBBBSCrocException
