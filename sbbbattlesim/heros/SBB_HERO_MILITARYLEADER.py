import logging

from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.heros import Hero

logger = logging.getLogger(__name__)


class LastBreathConvertedToOnAttackAndKillEvent(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, stack, *args, **kwargs):
        with stack.open() as executor:
            executor.execute(self.on_death_event, *args, **kwargs)


class HeroType(Hero):
    display_name = 'Trophy Hunter'
    aura = True

    def buff(self, target_character, *args, **kwargs):
        for on_death_event in target_character.get('OnDeath'):
            if on_death_event.last_breath:
                target_character.register(LastBreathConvertedToOnAttackAndKillEvent, temp=True,
                                          on_death_event=on_death_event)
