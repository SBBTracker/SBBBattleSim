from sbbbattlesim.characters import Character
from sbbbattlesim.combat import attack
from sbbbattlesim.events import OnStart
import logging

from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Lightning Dragon'

    flying = True

    _attack = 10
    _health = 1
    _level = 4
    _tribes = {Tribe.DRAGON}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class LightningDragonOnStart(OnStart):
            lightning_dragon = self
            def handle(self, *args, **kwargs):
                attack(
                    attack_position=self.lightning_dragon.position,
                    attacker=self.manager,
                    defender=self.manager.opponent,
                )

        self.owner.register(LightningDragonOnStart)

