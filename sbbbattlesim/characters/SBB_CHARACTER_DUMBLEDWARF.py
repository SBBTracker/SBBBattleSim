from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnBuff
import logging

from sbbbattlesim.utils import StatChangeCause

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Dubly'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.DublyOnBuff)

    class DublyOnBuff(OnBuff):
        def handle(self, attack_buff=0, health_buff=0, temp=False, *args, **kwargs):
            golden_multiplier = 2 if self.manager.golden else 1
            self.manager.change_stats(
                health=health_buff * golden_multiplier,
                attack=attack_buff * golden_multiplier,
                temp=temp,
                reason=StatChangeCause.DOUBLEY_BUFF,
                source=self
            )
