from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Easter Egg'

    def buff(self, target_character):
        if target_character.golden:
            target_character.change_stats(attack=3, health=3, reason=209, source=self, temp=True)
