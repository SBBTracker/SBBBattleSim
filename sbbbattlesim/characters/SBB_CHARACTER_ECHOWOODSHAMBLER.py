from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnBuff, OnSummon
import logging

from sbbbattlesim.utils import Tribe, StatChangeCause

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Echowood Dryad'
    aura = True

    _attack = 1
    _health = 1
    _level = 6
    _tribes = {Tribe.TREANT}

    def buff(self, target_character, *args, **kwargs):
        if target_character.id is not self.id:

            class EchoWoodBuff(OnBuff):
                echo_wood = self

                def handle(self, stack, force_echowood=None, attack=0, health=0, damage=0, reason='', temp=True, *args, **kwargs):
                    if not temp or force_echowood:

                        gold_multiplier = 2 if self.echo_wood.golden else 1

                        self.echo_wood.change_stats(
                            attack=gold_multiplier * attack,
                            health=gold_multiplier * health,
                            temp=False,
                            reason=StatChangeCause.ECHOWOOD_BUFF, source=self.manager,
                            stack=stack
                        )

            target_character.register(EchoWoodBuff, temp=True)

