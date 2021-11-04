from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Noble Steed'

    def buff(self, target_character):
        if 'quest' in target_character.tribes:
            target_character.change_stats(health=1, attack=1, reason=f'{self} aura', temp=True)