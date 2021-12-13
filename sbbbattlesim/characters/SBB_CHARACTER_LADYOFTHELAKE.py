from sbbbattlesim.action import Buff, SupportBuff
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.support_buff = SupportBuff(source=self, health=10 if self.golden else 5, temp=True,)

    def buff(self, target_character, *args, **kwargs):
        self.support_buff.execute(target_character, *args, **kwargs)
