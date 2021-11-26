from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnBuff
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

    def buff(self, target_character):
        if target_character.id != self.id:

            class EchoWoodBuff(OnBuff):
                echo_wood = self
                gold_multiplier = 2 if echo_wood.golden else 1
                def handle(self, attack_buff=0, health_buff=0, temp=False, *args, **kwargs):
                    if not temp:
                        self.echo_wood.change_stats(
                            attack=self.gold_multiplier*attack_buff,
                            health=self.gold_multiplier*health_buff,
                            temp=False,
                            reason=StatChangeCause.ECHOWOOD_BUFF, source=self.manager
                        )

            target_character.register(EchoWoodBuff, temp=True)

