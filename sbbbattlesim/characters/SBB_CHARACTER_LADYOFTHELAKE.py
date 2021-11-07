from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause


class CharacterType(Character):
    display_name = 'Lady of the Lake'
    support = True

    def buff(self, target_character):
        target_character.change_stats(health=10 if self.golden else 5, temp=True, reason=StatChangeCause.SUPPORT_BUFF, source=self)
