from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe
from sbbbattlesim.action import Buff, ActionReason, Aura


class CharacterType(Character):
    display_name = 'Princess Wight'
    aura = True
    quest = True

    _attack = 2
    _health = 4
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.PRINCESS}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        modifier = 2 if self.golden else 1
        self.aura = Aura(reason=ActionReason.PRINCESS_WIGHT_BUFF, source=self, attack=modifier, health=modifier,
                         _lambda=lambda char: Tribe.DWARF in char.tribes)
