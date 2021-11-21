from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath


class TreasureType(Treasure):
    display_name = 'Phoenix Feather'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feather_used = False

        class PhoenixFeatherSummon(OnDeath):
            feather = self
            last_breath = True
            def handle(self, *args, **kwargs):
                if not self.feather.feather_used and self.manager.attack == sorted(self.manager.owner.board, key=lambda char: char.attack, reverse=True)[0]:
                    self.manager.owner.graveyard.remove(self.manager)
                    self.manager.owner.summon(self.manager.position, self.manager)
        self.player.register(PhoenixFeatherSummon)



