from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import random_combat_spell

class TreasureType(Treasure):
    display_name = 'The Ninth Book of Merlin'

    def buff(self, target_character):

        class NinthBookOnDeath(OnDeath):
            book = self
            last_breath = True

            def handle(self, *args, **kwargs):
                for _ in range(bool(self.book.mimic)+ 1):
                    random_combat_spell(self.manager.owner.level).cast()

        target_character.register(NinthBookOnDeath)
        target_character.last_breath = True