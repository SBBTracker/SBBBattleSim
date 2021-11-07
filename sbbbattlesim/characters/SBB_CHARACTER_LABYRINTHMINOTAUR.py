from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause


class CharacterType(Character):
    display_name = 'Labyrinth Minotaur'
    aura = True

    def buff(self, target_character):
        if 'evil' in target_character.tribes and target_character != self:
            target_character.change_stats(attack=2 if self.golden else 1, temp=True, reason=StatChangeCause.AURA_BUFF, source=self)
