from sbbbattlesim.action import Buff, Support, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Boom Hilda'
    support = True
    ranged = True

    _attack = 10
    _health = 5
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.MONSTER, Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.support = Support(source=self, attack=20 if self.golden else 10)
