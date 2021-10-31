from sbbbattlesim.characters import Character
import logging

from sbbbattlesim.events import OnStart

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Shoulder Faeries'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class FairyBuffOnStart(OnStart):
            shoulder_faeries = self
            def handle(self, *args, **kwargs):
                highest_attack_evil = max(char.attack for char in self.manager.valid_characters() if 'evil' in char.tribes)
                highest_health_good = max(char.health for char in self.manager.valid_characters() if 'good' in char.tribes)
                self.shoulder_faeries.change_stats(attack=highest_attack_evil, health=highest_health_good,
                                                   temp=False, reason=f'{self.shoulder_faeries} OnStart Buff')
                logger.debug(self.shoulder_faeries)

        self.owner.register(FairyBuffOnStart)
