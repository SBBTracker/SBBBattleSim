from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Fairy Queen\'s Wand'

    def buff(self, target_character):
        target_character.change_stats(health=5, attack=5, reason=f'{self} aura', temp=True)