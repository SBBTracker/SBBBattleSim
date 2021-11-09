from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Ring of Rage'

    def buff(self, target_character):
        target_character.change_stats(attack=3, reason=222, source=self, temp=True)