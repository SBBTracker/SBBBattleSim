from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Power Orb'
    aura = True

    def buff(self, target_character):
        for _ in range(self.mimic + 1):
            target_character.change_stats(health=1, attack=1, reason=StatChangeCause.POWER_ORB, source=self, temp=True)
