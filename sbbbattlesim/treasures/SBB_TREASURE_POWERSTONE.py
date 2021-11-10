from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Power Orb'

    def buff(self, target_character):
        target_character.change_stats(health=1, attack=1, reason=218, source=self, temp=True)