from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe, StatChangeCause


class CharacterType(Character):
    display_name = 'Good Witch of the North'
    support = True

    _attack = 2
    _health = 3
    _level = 3
    _tribes = {Tribe.GOOD, Tribe.MAGE}

    def buff(self, target_character):
        if Tribe.GOOD in target_character.tribes:
            golden_multiplyer = 2 if self.golden else 1
            target_character.change_stats(
                attack=2*golden_multiplyer,
                health=3*golden_multiplyer,
                temp=True,
                reason=StatChangeCause.SUPPORT_BUFF, source=self
            )
