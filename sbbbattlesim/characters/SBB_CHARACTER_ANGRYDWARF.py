from sbbbattlesim.action import Buff, SupportBuff
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Fanny'
    support = True

    _attack = 2
    _health = 2
    _level = 2
    _tribes = {Tribe.DWARF, }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stat_change = 4 if self.golden else 2
        self.support_buff = SupportBuff(source=self, _lambda=lambda char: Tribe.DWARF in char.tribes,
                                        health=stat_change, attack=stat_change)

    def buff(self, target_character, *args, **kwargs):
        self.support_buff.execute(target_character, *args, **kwargs)
