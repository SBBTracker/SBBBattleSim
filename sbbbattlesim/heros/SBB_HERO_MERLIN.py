import logging
import random

from sbbbattlesim.events import OnDeath, OnSpellCast
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe, StatChangeCause


logger = logging.getLogger(__name__)


class HeroType(Hero):
    display_name = 'Merlin'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class MerlinOnSpellCast(OnSpellCast):
            merlin = self
            def handle(self, caster, spell, target, *args, **kwargs):
                logger.debug(f'ON CAST {caster} {spell} {target}')
                valid_targets = self.manager.valid_characters()
                logger.debug(f'MERLIN TARGET {valid_targets}')
                if valid_targets:
                    target_character = random.choice(valid_targets)
                    target_character.change_stats(attack=2, health=1, reason=StatChangeCause.MERLIN_BUFF, source=self.merlin, temp=False)

        self.player.register(MerlinOnSpellCast)