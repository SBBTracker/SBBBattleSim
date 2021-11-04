from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Sky Castle'

    def buff(self, target_character):
        if 'prince' in target_character.tribes or 'princess' in target_character.tribes:
            target_character.change_stats(health=4, attack=4, reason=f'{self} aura', temp=True)