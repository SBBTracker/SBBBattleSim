from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Sheperd\'s Sling'

    def buff(self, target_character):
        if 3 <= target_character.cost:
            target_character.change_stats(health=1, attack=1, reason=f'{self} aura', temp=True)