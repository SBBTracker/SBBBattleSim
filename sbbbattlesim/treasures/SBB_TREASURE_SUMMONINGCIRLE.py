from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnSummon
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Summoning Portal'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buff_count = 0

        class SummoningPortalBuff(OnSummon):

            def handle(self, summoned_characters, *args, **kwargs):
                summoned_characters = summoned_characters
                for char in summoned_characters:
                    self.buff_count += 1
                    char.change_stats(attack=self.buff_count, health=self.buff_count, reason=StatChangeCause.SUMMONING_PORTAL)

        self.player.register(SummoningPortalBuff)

