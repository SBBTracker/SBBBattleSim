from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath
import random
import logging

logger = logging.getLogger(__name__)

class AncientSarcophagusOnDeath(OnDeath):
    def handle(self, dead_thing, *args, **kwargs):
        itr = 1 # TODO this may be useful when dealing with mimic

        for _ in range(itr):
            valid_targets = self.manager.owner.opponent.valid_characters()

            if valid_targets:
                target = random.choice(valid_targets)
                target.damage += 3


class TreasureType(Treasure):
    name = 'Ancient Sarcophagus'
    aura = True

    def buff(self, target_character):
        if 'evil' in target_character.tribes:
            target_character.register(AncientSarcophagusOnDeath, temp=True)

