from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Sword of Fire and Ice'

    def buff(self, target_character):
        if 4 <= target_character.position:
            target_character.change_stats(health=5, reason=f'{self} aura', temp=True)
        else:
            target_character.change_stats(attack=5, reason=f'{self} aura', temp=True)
