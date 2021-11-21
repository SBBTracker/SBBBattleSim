from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Sword of Fire and Ice'
    aura = True

    def buff(self, target_character):
        if 4 <= target_character.position:
            for _ in range(bool(self.mimic) + 1):
                target_character.change_stats(health=6, reason=StatChangeCause.SWORD_OF_FIRE_AND_ICE, source=self,
                                              temp=True)
        else:
            for _ in range(bool(self.mimic) + 1):
                target_character.change_stats(attack=6, reason=StatChangeCause.SWORD_OF_FIRE_AND_ICE, source=self,
                                              temp=True)
