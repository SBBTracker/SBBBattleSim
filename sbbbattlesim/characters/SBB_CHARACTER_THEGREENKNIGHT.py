from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'The Green Knight'
    support = True

    _attack = 10
    _health = 30
    _level = 6
    _tribes = {Tribe.GOOD, Tribe.TREANT}

    def buff(self, target_character):
        target_character.change_stats(health=20 if self.golden else 10, temp=True, reason=StatChangeCause.SUPPORT_BUFF, source=self)
