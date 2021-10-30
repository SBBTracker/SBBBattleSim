from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnBuff
import logging

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Echowood Dryad'
    aura = True

    def buff(self, target_character):
        if target_character.id != self.id:

            class EchoWoodBuff(OnBuff):
                echo_wood = self
                def handle(self, attack_buff=0, health_buff=0, *args, **kwargs):
                    self.echo_wood._base_attack += attack_buff
                    self.echo_wood._base_health += health_buff

            target_character.register(EchoWoodBuff)

