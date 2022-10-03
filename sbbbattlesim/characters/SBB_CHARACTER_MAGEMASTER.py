from sbbbattlesim.action import Buff, Support, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Sporko'
    support = True
    ranged = True

    _attack = 2
    _health = 2
    _level = 4
    _tribes = {Tribe.EVIL, Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.support = Support(source=self, attack=8 if self.golden else 4)
