import logging

from sbbbattlesim.action import Buff
from sbbbattlesim.events import OnPreStart
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe, StatChangeCause

logger = logging.getLogger(__name__)


class FallenAngelOnStart(OnPreStart):
    def handle(self, *args, **kwargs):
        self.angel.angel_attack_buff = len(
            self.angel.player.valid_characters(_lambda=lambda char: Tribe.EVIL in char.tribes)) >= 3
        self.angel.angel_health_buff = len(
            self.angel.player.valid_characters(_lambda=lambda char: Tribe.GOOD in char.tribes)) >= 3


class HeroType(Hero):
    display_name = 'Fallen Angel'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.angel_attack_buff = False
        self.angel_health_buff = False

        self.player.register(FallenAngelOnStart, angel=self)

    def buff(self, target_character, *args, **kwargs):
        if self.angel_health_buff or self.angel_attack_buff:
            attack_buff = 2 if self.angel_attack_buff else 0
            health_buff = 2 if self.angel_health_buff else 0

            Buff(reason=StatChangeCause.FALLEN_ANGEL_BUFF, source=self, targets=[target_character],
                 attack=attack_buff, health=health_buff, temp=True, *args, **kwargs).resolve()
