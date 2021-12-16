import logging

from sbbbattlesim.action import Aura
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.heros import Hero

logger = logging.getLogger(__name__)


class LastBreathConvertedToOnAttackAndKillEvent(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, *args, **kwargs):
        self.on_death_event(*args, **kwargs)


def convert_on_death_to_on_attack_and_kill(char):
    for on_death_event in char.get('OnDeath'):
        if on_death_event.last_breath:
            char.register(LastBreathConvertedToOnAttackAndKillEvent, temp=True, on_death_event=on_death_event)


class HeroType(Hero):
    display_name = 'Trophy Hunter'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura_buff = Aura(_action=convert_on_death_to_on_attack_and_kill)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
