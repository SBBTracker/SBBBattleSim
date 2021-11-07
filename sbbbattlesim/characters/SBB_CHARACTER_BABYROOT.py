from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause


class CharacterType(Character):
    display_name = 'Baby Root'
    support = True

    def buff(self, target_character):
        target_character.change_stats(health=6 if self.golden else 3, temp=True,
                                      reason=StatChangeCause.SUPPORT_BUFF, source=self)
