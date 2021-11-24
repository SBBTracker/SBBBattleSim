from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.exceptions import SBBSBCrocException
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Captain Croc'
    last_breath = True

    _attack = 10
    _health = 10
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        raise SBBSBCrocException