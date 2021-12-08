from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Bossy'
    aura = True

    _attack = 4
    _health = 4
    _level = 4
    _tribes = {Tribe.DWARF}

    def buff(self, target_character, *args, **kwargs):
        if Tribe.DWARF in target_character.tribes and target_character != self:
            modifier = 4 if self.golden else 2
            with Buff(reason=StatChangeCause.AURA_BUFF, source=self, targets=[target_character],
                      attack=modifier, health=modifier, temp=True, *args, **kwargs):
                pass
