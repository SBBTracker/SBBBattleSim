from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.events import OnBuff
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Singing Swords'

    _level = 6

    aura = True

    def buff(self, target_character, attack_override, *args, **kwargs):
        if '''SBB_TREASURE_TREASURECHEST''' in target_character.player.treasures:
            attack_multiplier = 2
        else:
            attack_multiplier = 1

        if target_character.position in [1, 2, 3, 4]:
            Buff(targets=[target_character], attack=attack_override*attack_multiplier, source=self, reason=ActionReason.SINGINGSWORD_BUFF, temp=True, *args, **kwargs).resolve()
