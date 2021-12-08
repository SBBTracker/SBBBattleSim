from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'The Green Knight'
    support = True

    _attack = 10
    _health = 30
    _level = 6
    _tribes = {Tribe.GOOD, Tribe.TREANT}

    def buff(self, target_character, *args, **kwargs):
        with Buff(reason=StatChangeCause.SUPPORT_BUFF, source=self, targets=[target_character],
                  health=20 if self.golden else 10, temp=True, *args, **kwargs):
            pass
