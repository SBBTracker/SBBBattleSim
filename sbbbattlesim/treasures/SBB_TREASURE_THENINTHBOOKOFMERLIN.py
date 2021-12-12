import logging

from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import random_combat_spell, Tribe

logger = logging.getLogger(__name__)


class NinthBookOnDeath(OnDeath):
    last_breath = True

    def handle(self, *args, **kwargs):
        for _ in range(bool(self.book.mimic) + 1):
            spell = random_combat_spell(self.manager.player.level)
            if spell:
                self.manager.player.cast(spell)


class TreasureType(Treasure):
    display_name = 'The Ninth Book of Merlin'
    aura = True

    _level = 5

    def buff(self, target_character, *args, **kwargs):
        if Tribe.MAGE in target_character.tribes:
            for _ in range(1 + bool(self.mimic)):
                target_character.register(NinthBookOnDeath, temp=True, book=self)
