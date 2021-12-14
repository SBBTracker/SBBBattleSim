import logging

from sbbbattlesim.action import EventAura
from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import random_combat_spell, Tribe

logger = logging.getLogger(__name__)


class NinthBookOnDeath(OnDeath):
    last_breath = True
    # TODO Does this trigger twice or are there two last breaths
    def handle(self, *args, **kwargs):
        for _ in range(bool(self.book.mimic) + 1):
            spell = random_combat_spell(self.manager.player.level)
            if spell:
                self.manager.player.cast(spell)


class TreasureType(Treasure):
    display_name = 'The Ninth Book of Merlin'
    aura = True

    _level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura_buff = EventAura(event=NinthBookOnDeath, source=self, book=self,
                                  _lambda=lambda char: Tribe.MAGE in char.tribes)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
