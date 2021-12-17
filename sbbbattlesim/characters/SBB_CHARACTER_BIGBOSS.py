from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Bossy'
    aura = True

    _attack = 4
    _health = 4
    _level = 4
    _tribes = {Tribe.DWARF}

    deactivated = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        modifier = 4 if self.golden else 2
        self.aura_buff = Aura(reason=ActionReason.AURA_BUFF, source=self, attack=modifier, health=modifier,
                              _lambda=lambda char: Tribe.DWARF in char.tribes)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
