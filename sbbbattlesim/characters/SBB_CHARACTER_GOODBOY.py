from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
import logging

logger = logging.getLogger(__name__)


class CharacterType(Character):
    display_name = 'Good Boy'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.GoodBoyDeath)

    class GoodBoyDeath(OnDeath):
        def handle(self, *args, **kwargs):
            golden_multiplyer = 2 if self.manager.golden else 1
            attack_buff = self.manager.attack * golden_multiplyer
            health_buff = (self.manager.base_health + self.manager.health_bonus) * golden_multiplyer

            for char in self.manager.owner.valid_characters():
                if 'good' in char.tribes:
                    char.base_health += health_buff
                    char.base_attack += attack_buff
