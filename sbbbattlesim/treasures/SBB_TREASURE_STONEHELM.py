from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Haunted Helm'

    def buff(self, target_character):
        if 1 == target_character.position:
            target_character.change_stats(health=10, reason=f'{self} aura', temp=True)