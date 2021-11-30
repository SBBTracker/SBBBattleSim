from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Baby Root'
    support = True

    _attack = 0
    _health = 3
    _level = 2
    _tribes = {Tribe.GOOD, Tribe.TREANT}

    def buff(self, target_character, *args, **kwargs):
        target_character.change_stats(health=6 if self.golden else 3, temp=True, reason=StatChangeCause.SUPPORT_BUFF,
                                      source=self, *args, **kwargs)
