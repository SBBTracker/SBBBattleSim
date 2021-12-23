import logging

from sbbbattlesim.action import Aura, ActionReason
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.heros import Hero

logger = logging.getLogger(__name__)


class LastBreathConvertedToOnAttackAndKillEvent(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, stack, *args, **kwargs):
        with stack.open() as executor:
            executor.execute(self.source, reason=ActionReason.TROPHY_HUNTER_PROC, *args, **kwargs)


def convert_on_death_to_on_attack_and_kill(char):
    for on_death_event in char.get('OnDeath'):
        if on_death_event.last_breath:
            char.register(LastBreathConvertedToOnAttackAndKillEvent, source=on_death_event)


class HeroType(Hero):
    display_name = 'Trophy Hunter'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(_action=convert_on_death_to_on_attack_and_kill, source=self)
