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
            def handle(self, summoned_characters, stack, *args, **kwargs):
                level = self.geppetto.player.level
                for char in summoned_characters:
                    char.change_stats(attack=level, health=level, reason=StatChangeCause.GEPPETTO_BUFF, source=self.geppetto, stack=stack)

        self.player.register(GeppettoOnSummon)