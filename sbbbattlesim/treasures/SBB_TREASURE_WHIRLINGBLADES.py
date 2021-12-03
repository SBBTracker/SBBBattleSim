from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnBuff
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Singing Swords'

    _level = 6

    aura = True


    def buff(self, target_character, *args, **kwargs):

        class SingingSwordOnBuff(OnBuff):
            def handle(self, stack, force_echowood=None, attack=0, health=0, damage=0, reason='', temp=True, *args, **kwargs):
                if reason is StatChangeCause.SINGINGSWORD_BUFF:
                    return

                if '''SBB_TREASURE_TREASURECHEST''' in self.manager.owner.treasures:
                    attack_multiplier = 2
                else:
                    attack_multiplier = 1

                self.manager.change_stats(
                    attack=attack*attack_multiplier,
                    source=self,
                    reason=StatChangeCause.SINGINGSWORD_BUFF,
                    temp=temp,
                )

        if target_character.position in [1, 2, 3, 4]:
            target_character.register(SingingSwordOnBuff, temp=True)

