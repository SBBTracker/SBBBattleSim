from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause


class CharacterType(Character):
    display_name = 'Sporko'
    support = True

    def buff(self, target_character):
        target_character.change_stats(attack=10 if self.golden else 5, temp=True, reason=StatChangeCause.SUPPORT_BUFF, source=self)
