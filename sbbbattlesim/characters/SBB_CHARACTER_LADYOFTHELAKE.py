from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Lady of the Lake'
    support = True
    ranged = True

    _attack = 3
    _health = 3
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.MAGE}

    def buff(self, target_character, *args, **kwargs):
        target_character.change_stats(health=10 if self.golden else 5, temp=True, reason=StatChangeCause.SUPPORT_BUFF,
                                      source=self, *args, **kwargs)
