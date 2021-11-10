from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Fountain Of Youth'

    def buff(self, target_character):
        target_character.change_stats(health=1, reason=212,source=self, temp=True)