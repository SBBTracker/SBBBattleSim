from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath


class TreasureType(Treasure):
    display_name = 'Phoenix Feather'
    # todo implement me

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feather_used = False

    def buff(self, target_character):
        class PhoenixFeatherSummon(OnDeath):
            if not self.feather_used and self.manager.attack == sorted(self.manager.owner.board, key=lambda char: char.attack, reverse=True)[0]:
            self.manager.owner.graveyard.remove(self.manager)
            self.manager.owner.summon(self.manager.position, self.manager)
        target_character.register(PhoenixFeatherSummon)



