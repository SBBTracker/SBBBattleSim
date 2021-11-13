import random

from sbbbattlesim.events import OnDeath, OnSummon
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import StatChangeCause, Tribe


class HeroType(Hero):
    display_name = 'Mirhi, King Lion'
    aura = True

    def __init__(self, mirhi_buff=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mirhi_buff = mirhi_buff

    def buff(self, target_character):
        if Tribe.PRINCE in target_character.tribes or Tribe.PRINCESS in target_character.tribes:
            target_character.change_stats(attack=1*self.mirhi_buff, health=2*self.mirhi_buff, reason=StatChangeCause.MIRHI_BUFF, source=self)