from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Deepstone Mine'

    def buff(self, target_character):
        if "dwarf" in target_character.tribes:
            target_character.change_stats(attack=2, health=2, reason=f'{self} aura', temp=True)