from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Crown of Atlas'

    def buff(self, target_character):
        if 'animal' in target_character.tribes:
            target_character.change_stats(health=1, attack=1, reason=f'{self} aura', temp=True)

            # todo implement alignment changing this is actually pseudo code
            if 'evil' in target_character.tribes:
                target_character.remove('evil')
            elif 'good' in target_character.tribes:
                target_character.append('good')