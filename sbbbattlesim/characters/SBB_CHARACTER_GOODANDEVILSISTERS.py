from sbbbattlesim.characters import Character
import logging

from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import StatChangeCause, Tribe

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Shoulder Faeries'

    _attack = 1
    _health = 1
    _level = 5
    _tribes = {Tribe.FAIRY}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class FairyBuffOnStart(OnStart):
            shoulder_faeries = self
            def handle(self, *args, **kwargs):
                highest_attack_evil = max([char.attack for char in self.manager.valid_characters(_lambda=lambda char: Tribe.EVIL in char.tribes)] + [0])
                highest_health_good = max([char.health for char in self.manager.valid_characters() if Tribe.GOOD in char.tribes] + [0])
                self.shoulder_faeries.change_stats(
                    attack=highest_attack_evil * (2 if self.shoulder_faeries.golden else 1),
                    health=highest_health_good * (2 if self.shoulder_faeries.golden else 1),
                    temp=False,
                    reason=StatChangeCause.SHOULDER_FAIRY_BUFF,
                    source=self.shoulder_faeries
                )

        self.owner.register(FairyBuffOnStart)
