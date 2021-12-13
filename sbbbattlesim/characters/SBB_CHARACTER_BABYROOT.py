from sbbbattlesim.action import Buff, SupportBuff
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Baby Root'
    support = True

    _attack = 0
    _health = 3
    _level = 2
    _tribes = {Tribe.GOOD, Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.support_buff = SupportBuff(source=self, health=6 if self.golden else 3)

    def buff(self, target_character, *args, **kwargs):
        self.support_buff.execute(target_character, *args, **kwargs)
