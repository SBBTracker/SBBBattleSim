import logging

from sbbbattlesim.action import Aura
from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import random_combat_spell, Tribe

logger = logging.getLogger(__name__)


class NinthBookOnDeath(OnDeath):
    last_breath = True

    # TODO Does this trigger twice or are there two last breaths
    def handle(self, stack, reason, *args, **kwargs):
        spell = random_combat_spell(self.manager.player.level)
        if spell:
            self.manager.player.cast_spell(spell.id)


class TreasureType(Treasure):
    display_name = 'The Ninth Book of Merlin'
    aura = True

    _level = 6

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(event=NinthBookOnDeath, source=self, _lambda=lambda char: Tribe.MAGE in char.tribes,
                         multiplier=self.mimic + 1)
