from sbbbattlesim.events import OnBuff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Singing Swords'

    _level = 6

    aura = True


    def buff(self, target_character, attack_override, *args, **kwargs):
        if '''SBB_TREASURE_TREASURECHEST''' in target_character.owner.treasures:
            attack_multiplier = 2
        else:
            attack_multiplier = 1

        if target_character.position in [1, 2, 3, 4]:
            target_character.change_stats(attack=attack_override*attack_multiplier, source=self, reason=StatChangeCause.SINGINGSWORD_BUFF, temp=True, *args, **kwargs)
