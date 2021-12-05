import logging
import random

from sbbbattlesim.events import OnDeath, OnSpellCast, OnAttackAndKill
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe, StatChangeCause


logger = logging.getLogger(__name__)


class HeroType(Hero):
    display_name = 'Trophy Hunter'
    aura = True

    def buff(self, target_character, *args, **kwargs):
        for on_death_event in target_character.get('OnDeath'):
            if on_death_event.last_breath:

                self._register_trophyhunter_event(on_death_event, target_character, *args, **kwargs)

    def _register_trophyhunter_event(self, on_death_event, target_character, *args, **kwargs):
        class LastBreathConvertedToOnAttackAndKillEvent(OnAttackAndKill):
            slay = True

            def handle(self, killed_character, *args, **kwargs):
                on_death_event(*args, **kwargs)

        target_character.register(LastBreathConvertedToOnAttackAndKillEvent, temp=True)

