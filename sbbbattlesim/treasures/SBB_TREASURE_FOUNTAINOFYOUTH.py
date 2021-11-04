from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Fountain Of Youth'

    def buff(self, target_character):
        target_character.change_stats(health=1, reason=f'{self} aura', temp=True)