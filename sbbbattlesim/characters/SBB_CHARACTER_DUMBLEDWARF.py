from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnBuff
import logging

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Dubly'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.DublyOnBuff)

    class DublyOnBuff(OnBuff):
        def handle(self, attack_buff=0, health_buff=0, temp=False, *args, **kwargs):
            logger.info(f'SUP SLUTS PASSING IN ATTACK BUFF OF {attack_buff} AND HEALTH BUFF OF {health_buff}')
            logger.info(f'THIS IS ME BEFORE THE BUFF: {self.manager}')
            golden_multiplier = 2 if self.manager.golden else 1
            if temp:
                self.manager._attack_bonus += attack_buff * golden_multiplier
                self.manager._health_bonus += health_buff * golden_multiplier
            else:
                self.manager._base_attack += attack_buff * golden_multiplier
                self.manager._base_health += health_buff * golden_multiplier
            logger.info(f'THIS IS ME AFTER THE BUFF: {self.manager}')
