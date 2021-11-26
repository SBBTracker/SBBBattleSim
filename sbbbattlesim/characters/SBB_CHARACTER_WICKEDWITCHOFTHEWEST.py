from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Wicked Witch of the West'
    support = True

    _attack = 3
    _health = 2
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.MAGE}

    def buff(self, target_character):
        if Tribe.EVIL in target_character.tribes:
            golden_multiplyer = 2 if self.golden else 1
            target_character.change_stats(
                attack=3*golden_multiplyer,
                health=2*golden_multiplyer,
                temp=True,
                reason=StatChangeCause.SUPPORT_BUFF,
                source=self
            )
