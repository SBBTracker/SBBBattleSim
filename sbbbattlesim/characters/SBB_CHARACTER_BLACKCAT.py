import sbbbattlesim
from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe
import logging

logger = logging.getLogger(__name__)


class BlackCatLastBreath(OnDeath):
    last_breath = True

    def handle(self, stack, reason, *args, **kwargs):
        stat = 2 if self.manager.golden else 1
        cat = character_registry['SBB_CHARACTER_CAT'](
            self.manager.player,
            self.manager.position,
            stat,
            stat,
            golden=False,
            keywords=[],
            tribes=['evil', 'animal'],
            cost=1
        )

        self.manager.player.summon(self.manager.position, [cat], *args, **kwargs)


class CharacterType(Character):
    display_name = 'Black Cat'
    last_breath = True

    _attack = 1
    _health = 1
    _level = 2
    _tribes = {Tribe.EVIL, Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(BlackCatLastBreath)
