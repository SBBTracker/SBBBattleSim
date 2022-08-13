from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe
from sbbbattlesim.action import Buff, ActionReason, Aura


class CharacterType(Character):
    display_name = 'Princess Wight'
    aura = True
    quest = True

    _attack = 3
    _health = 5
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.ROYAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
