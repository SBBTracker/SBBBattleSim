from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause


class CharacterType(Character):
    display_name = 'Bossy'
    aura = True

    def buff(self, target_character):
        if 'dwarf' in target_character.tribes and target_character != self:
            modifier = 4 if self.golden else 2
            target_character.change_stats(attack=modifier, health=modifier, temp=True, reason=StatChangeCause.AURA_BUFF, source=self)
