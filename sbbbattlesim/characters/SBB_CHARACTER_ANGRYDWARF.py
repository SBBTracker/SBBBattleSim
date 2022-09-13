from sbbbattlesim.action import Buff, Support, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Fanny'
    support = True

    _attack = 4
    _health = 4
    _level = 4
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stat_change = 8 if self.golden else 4
        self.support = Support(source=self, _lambda=lambda char: Tribe.DWARF in char.tribes,
                               health=stat_change, attack=stat_change)
