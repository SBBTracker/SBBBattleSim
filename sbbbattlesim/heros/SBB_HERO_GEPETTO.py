import random

from sbbbattlesim.events import OnDeath, OnSummon
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import StatChangeCause


class HeroType(Hero):
    display_name = 'Geppetto'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class GeppettoOnSummon(OnSummon):
            geppetto = self
            def handle(self, summoned_characters, *args, **kwargs):
                for char in summoned_characters:
                    char.change_stats(attack=3, health=3, reason=StatChangeCause.GEPPETTO_BUFF, source=self.geppetto)

        self.player.register(GeppettoOnSummon)