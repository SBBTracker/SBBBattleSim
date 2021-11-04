from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Corrupted Heartwood'

    def buff(self, target_character):
        if 'animal' in target_character.tribes or 'treant' in target_character.tribes:
            target_character.change_stats(attack=1, reason=f'{self} aura', temp=True)

            # todo implement alignment changing this is actually pseudo code
            if 'good' in target_character.tribes:
                target_character.remove('good')
            elif 'evil' in target_character.tribes:
                target_character.append('evil')