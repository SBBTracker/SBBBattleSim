from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath

#todo update spell list
class TreasureType(Treasure):
    display_name = 'The Ninth Book of Merlin'

    def buff(self, target_character):

        class NinthBookOnDeath(OnDeath):
            book = self
            last_breath = True

            def handle(self, *args, **kwargs):
                pass