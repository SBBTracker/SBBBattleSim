import logging

from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill, OnDeath
from sbbbattlesim.utils import get_behind_targets, Tribe
import random

logger = logging.getLogger(__name__)


class GrimSoulOnDeath(OnDeath):
    last_breath = True

    def handle(self, stack, reason, *args, **kwargs):
        targets = self.manager.player.valid_characters(lambda char: char.slay and char.id not in ['SBB_CHARACTER_CERBERUS', 'SBB_CHARACTER_LOBO'])
        if targets:
            target = random.choice(targets)
            itr = 2 if self.manager.golden else 1
            slays = [evt for evt in target.get('OnAttackAndKill') if evt.slay]
            for _ in range(itr):
                with stack.open(
                        killed_character=None) as executor:  # does golden grim soul open two stacks or just the one. If just the one, flip this w/ the above for loop
                    for slay in slays:
                        logger.debug(f'Grim soul Triggering OnAttackAndKill({args} {kwargs})')
                        executor.execute(slay, killed_character=None, *args, **kwargs)
                    executor._react_buffer = executor._react_buffer[:1]   # Listeners to Grim Soul should react only once, no matter how many slays Grim Soul runs


class CharacterType(Character):
    display_name = 'Grim Soul'

    _attack = 5
    _health = 1
    _level = 4
    _tribes = {Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(GrimSoulOnDeath)
