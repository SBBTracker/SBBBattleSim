import logging

from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import get_behind_targets, Tribe
import random

logger = logging.getLogger(__name__)

#todo write tests for me
class GrimSoulOnDeath(OnDeath):
    last_breath = True

    def handle(self, stack, *args, **kwargs):

        targets = self.manager.player.valid_characters(lambda char: char.last_breath and char.id!='SBB_CHARACTER_CERBERUS')
        if targets:
            target = random.choice(targets)
        else:
            return

        itr = 2 if self.manager.golden else 1
        for _ in range(itr):
            with stack.open(source=self) as executor:
                last_breaths = [evt for evt in target.get('OnDeath') if evt.last_breath]

                for lb in last_breaths:
                    logger.debug(f'Grimsoul Triggering LastBreath({args} {kwargs})')
                    executor.execute(lb, *args, **kwargs)


class CharacterType(Character):
    display_name = 'Grim Soul'

    _attack = 4
    _health = 1
    _level = 4
    _tribes = {Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(GrimSoulOnDeath)
