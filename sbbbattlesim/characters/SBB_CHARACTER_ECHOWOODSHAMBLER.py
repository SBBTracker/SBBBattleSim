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
                def handle(self, attack_buff=0, health_buff=0, temp=False, *args, **kwargs):
                    if not temp:
                        self.echo_wood.change_stats(attack=attack_buff, health=health_buff, temp=False,
                                                    reason=f'{self.manager} is getting buffed')

            target_character.register(EchoWoodBuff, temp=True)
