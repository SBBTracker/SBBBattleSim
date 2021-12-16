from sbbbattlesim.action import Buff, Support, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Good Witch of the North'
    support = True

    _attack = 2
    _health = 3
    _level = 3
    _tribes = {Tribe.GOOD, Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        golden_multiplyer = 2 if self.golden else 1
        self.support_buff = Support(source=self, _lambda=lambda char: Tribe.GOOD in char.tribes,
                                    attack=2 * golden_multiplyer, health=3 * golden_multiplyer)

    def buff(self, target_character, *args, **kwargs):
        self.support_buff.execute(target_character, *args, **kwargs)
