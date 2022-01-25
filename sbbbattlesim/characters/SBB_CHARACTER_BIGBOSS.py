from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Bossy'
    aura = True

    _attack = 6
    _health = 6
    _level = 5
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        modifier = 6 if self.golden else 3
        self.aura = Aura(reason=ActionReason.BOSSY_BUFF, source=self, attack=modifier, health=modifier,
                         _lambda=lambda char: Tribe.DWARF in char.tribes)
