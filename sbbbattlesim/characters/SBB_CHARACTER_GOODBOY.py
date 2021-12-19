import logging

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class GoodBoyDeath(OnDeath):
    last_breath = True

    def handle(self, stack, *args, **kwargs):
        golden_multiplyer = 2 if self.manager.golden else 1
        attack_buff = self.manager.attack * golden_multiplyer
        health_buff = (self.manager._base_health) * golden_multiplyer

        Buff(reason=ActionReason.GOODBOY_BUFF, source=self.manager,
             targets=self.manager.player.valid_characters(_lambda=lambda char: Tribe.GOOD in char.tribes),
             attack=attack_buff, health=health_buff, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Good Boy'
    last_breath = True

    _attack = 2
    _health = 2
    _level = 6
    _tribes = {Tribe.GOOD, Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(GoodBoyDeath)
