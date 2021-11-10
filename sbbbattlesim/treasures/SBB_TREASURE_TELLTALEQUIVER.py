from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Sting'

    def buff(self, target_character):
        if 5 <= target_character.position and 'ranged' in target_character.keywords:
            target_character.change_stats(health=3, attack=3, reason=231, source=self, temp=True)
