from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Grumble Gore'
    support = True
    ranged = True

    _attack = 10
    _health = 5
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def buff(self, target_character, *args, **kwargs):
        with Buff(reason=StatChangeCause.SUPPORT_BUFF, source=self, targets=[target_character],
                  attack=20 if self.golden else 10, temp=True,  *args, **kwargs):
            pass
