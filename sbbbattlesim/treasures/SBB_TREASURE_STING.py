from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Sting'

    def buff(self, target_character):
        if 1 == target_character.position:
            target_character.change_stats(attack=10, reason=228, source=self, temp=True)