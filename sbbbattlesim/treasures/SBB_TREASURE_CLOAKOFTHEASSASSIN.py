from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Cloak of the Assassin'

    def buff(self, target_character):
        if 'slay' in target_character.keywords:
            target_character.change_stats(health=3, attack=3, reason=205, source=self, temp=True)
