from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnBuff
import logging

from sbbbattlesim.utils import Tribe

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
                def handle(self, attack_buff=0, health_buff=0, temp=False, *args, **kwargs):
                    if not temp:
                        self.echo_wood.change_stats(attack=attack_buff, health=health_buff, temp=False,
                                                    reason=StatChangeCause.ECHOWOOD_BUFF, source=self.manager)

            target_character.register(EchoWoodBuff, temp=True)

