import logging

from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import random_combat_spell, Tribe


logger = logging.getLogger(__name__)


class TreasureType(Treasure):
    display_name = 'The Ninth Book of Merlin'
    aura = True

    def buff(self, target_character):
        logger.debug(f'{target_character.pretty_print()} Is this a mage??? {target_character.tribes} {Tribe.MAGE in target_character.tribes}')
        if Tribe.MAGE in target_character.tribes:
            class NinthBookOnDeath(OnDeath):
                book = self
                last_breath = True

                def handle(self, *args, **kwargs):
                    for _ in range(bool(self.book.mimic) + 1):
                        spell = random_combat_spell(self.manager.owner.level)
                        if spell:
                            self.manager.owner.cast(spell)

            for _ in range(1 + bool(self.mimic)):
                target_character.register(NinthBookOnDeath, temp=True)
            target_character.last_breath = True