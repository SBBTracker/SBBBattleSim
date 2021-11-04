from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Dancing Sword'

    def buff(self, target_character):
        target_character.change_stats(attack=1, reason=f'{self} aura', temp=True)