from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Six of Shields'

    def buff(self, target_character):
        target_character.change_stats(health=3, reason=f'{self} aura', temp=True)