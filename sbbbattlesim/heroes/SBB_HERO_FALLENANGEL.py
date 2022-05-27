import logging

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnSetup
from sbbbattlesim.heroes import Hero
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class FallenAngelOnSetup(OnSetup):
    def handle(self, *args, **kwargs):
        attack_buff = 2 if len(self.source.player.valid_characters(_lambda=lambda char: Tribe.EVIL in char.tribes)) >= 3 else 0
        health_buff = 2 if len(self.source.player.valid_characters(_lambda=lambda char: Tribe.GOOD in char.tribes)) >= 3 else 0

        self.source.aura.attack = attack_buff
        self.source.aura.health = health_buff


class HeroType(Hero):
    display_name = 'Fallen Angel'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(FallenAngelOnSetup, source=self, priority=100)
        self.aura = Aura(reason=ActionReason.FALLEN_ANGEL_BUFF, source=self, priority=1e99)
