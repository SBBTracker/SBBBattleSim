import logging

from sbbbattlesim import character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.spells import Spell

logger = logging.getLogger(__name__)

front_row_lambda = lambda char: char.position in (1, 2, 3, 4)


class CatsCallOnDeath(OnDeath):
    last_breath = False
    priority = 1000

    def handle(self, stack, reason, *args, **kwargs):
        if len(self.source.player.valid_characters(_lambda=front_row_lambda)) == 0:
            for pos in (1, 2, 3, 4):
                cat = character_registry['SBB_CHARACTER_CAT'].new(self.source.player, pos, False)
                self.source.player.summon_from_different_locations([cat])


class SpellType(Spell):
    display_name = '''Cat's Call'''
    _level = 4
    cost = 2

    def cast(self, target: 'Character' = None, *args, **kwargs):
        for char in self.player.valid_characters(_lambda=front_row_lambda):
            char.register(CatsCallOnDeath, temp=False, source=self)
