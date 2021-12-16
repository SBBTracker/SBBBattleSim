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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        modifier = 4 if self.golden else 2
        self.aura_buff = Aura(reason=ActionReason.AURA_BUFF, source=self, attack=modifier, health=modifier)

    def buff(self, target_character, *args, **kwargs):
        if Tribe.DWARF in target_character.tribes and target_character != self:
            self.aura_buff.execute(target_character)
