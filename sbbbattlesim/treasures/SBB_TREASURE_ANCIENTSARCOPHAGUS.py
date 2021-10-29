from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath
import random
import logging

logger = logging.getLogger(__name__)

class AncientSarcophagusOnDeath(OnDeath):
    def handle(self, dead_thing, *args, **kwargs):
        itr = 1 # TODO this may be useful when dealing with mimic

        for _ in range(itr):
            valid_targets = []
            for idx in self.manager.owner.opponent.characters:
                char = self.manager.owner.opponent.characters[idx]
                logger.info(f'One such character is {char}')
                if char is not None and not char.dead:
                    valid_targets.append(char)

            if valid_targets:
                target = random.choice(valid_targets)
                logger.info(f'My target is {target} in position {target.position}')
                target.damage += 3
                logger.info(f'My target was {target} in position {target.position}')
                logger.info(f'my targets are {self.manager.owner.opponent.characters.values()}')


class TreasureType(Treasure):
    name = 'Ancient Sarcophagus'
    aura = True

    def buff(self, target_character):
        if 'evil' in target_character.tribes:
            target_character.register(AncientSarcophagusOnDeath, temp=True)

