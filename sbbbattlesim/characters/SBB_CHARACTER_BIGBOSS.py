from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Bossy'
    aura = True

    _attack = 2
    _health = 2
    _level = 2
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        modifier = 2 if self.golden else 1
        self.aura = Aura(reason=ActionReason.BOSSY_BUFF, source=self, attack=modifier, health=modifier,
                         _lambda=lambda char: Tribe.DWARF in char.tribes)
