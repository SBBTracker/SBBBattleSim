import logging

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnStart
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class FallenAngelOnStart(OnStart):
    def handle(self, *args, **kwargs):
        attack_buff = 2 if len(self.angel.player.valid_characters(_lambda=lambda char: Tribe.EVIL in char.tribes)) >= 3 else 0
        health_buff = 2 if len(self.angel.player.valid_characters(_lambda=lambda char: Tribe.GOOD in char.tribes)) >= 3 else 0

        self.angel.aura.attack = attack_buff
        self.angel.aura.health = health_buff


class HeroType(Hero):
    display_name = 'Fallen Angel'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.player.board.register(FallenAngelOnStart, angel=self)

        self.aura = Aura(reason=ActionReason.FALLEN_ANGEL_BUFF, source=self, priority=1e99)

    
