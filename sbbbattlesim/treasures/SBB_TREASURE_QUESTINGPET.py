from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Keyword


class TreasureType(Treasure):
    display_name = 'Noble Steed'
    aura = True

    def buff(self, target_character):
        if target_character.quest:
            for _ in range(self.mimic + 1):
                target_character.change_stats(health=1, attack=1, reason=StatChangeCause.NOBLE_STEED, source=self, temp=True)
