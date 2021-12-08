from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Sporko'
    support = True
    ranged = True

    _attack = 3
    _health = 3
    _level = 4
    _tribes = {Tribe.EVIL, Tribe.MAGE}

    def buff(self, target_character, *args, **kwargs):
        with Buff(reason=StatChangeCause.SUPPORT_BUFF, source=self, targets=[target_character],
                  attack=10 if self.golden else 5, temp=True, *args, **kwargs):
            pass
