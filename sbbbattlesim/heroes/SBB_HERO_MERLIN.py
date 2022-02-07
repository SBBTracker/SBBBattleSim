import logging
import random

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.events import OnSpellCast
from sbbbattlesim.heroes import Hero

logger = logging.getLogger(__name__)


class MerlinOnSpellCast(OnSpellCast):
    def handle(self, caster, spell, target, stack, *args, **kwargs):
        logger.debug(f'ON CAST {caster} {spell} {target}')
        valid_targets = self.source.player.valid_characters()
        logger.debug(f'MERLIN TARGET {valid_targets}')
        if valid_targets:
            target_character = random.choice(valid_targets)
            Buff(reason=ActionReason.MERLIN_BUFF, source=self.source, targets=[target_character],
                 attack=1, health=1, temp=False, stack=stack).resolve()


class HeroType(Hero):
    display_name = 'Merlin'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(MerlinOnSpellCast, source=self)
