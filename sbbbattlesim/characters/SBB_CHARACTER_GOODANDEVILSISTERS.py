import logging

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class FairyBuffOnStart(OnStart):

    def handle(self, stack, *args, **kwargs):
        highest_attack_evil = max([char.attack for char in self.shoulder_faeries.player.valid_characters(_lambda=lambda char: Tribe.EVIL in char.tribes)] + [0])
        highest_health_good = max([char.health for char in self.shoulder_faeries.player.valid_characters() if Tribe.GOOD in char.tribes] + [0])
        Buff(reason=ActionReason.SHOULDER_FAIRY_BUFF, source=self.shoulder_faeries, targets=[self.shoulder_faeries],
             attack=highest_attack_evil * (2 if self.shoulder_faeries.golden else 1),
             health=highest_health_good * (2 if self.shoulder_faeries.golden else 1),
             temp=False).resolve()

class CharacterType(Character):
    display_name = 'Shoulder Faeries'

    _attack = 1
    _health = 1
    _level = 5
    _tribes = {Tribe.FAIRY}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.board.register(FairyBuffOnStart, priority=60, shoulder_faeries=self)
