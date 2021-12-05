import logging
import random

from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Great Pumpkin King'

    _attack = 5
    _health = 5
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class PumpkinKingOnDeath(OnDeath):
            last_breath = True

            def handle(self, *args, **kwargs):
                summons = []
                dead_in_order = sorted(
                    [char for char in self.manager.owner.graveyard if Tribe.EVIL in char.tribes],
                    key=lambda char: char._level, reverse=True
                )
                for dead in dead_in_order[:7]:
                    summon_choices = list(character_registry.filter(_lambda=lambda char: char._level == dead._level-1 and Tribe.EVIL in char._tribes))
                    if summon_choices:
                        summons.append(random.choice(summon_choices).new(
                            owner=self.manager.owner,
                            position=dead.position,
                            golden=self.manager.golden
                        ))

                self.manager.owner.summon_from_different_locations(summons)

        self.register(PumpkinKingOnDeath)