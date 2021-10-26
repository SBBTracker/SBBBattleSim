from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    name = 'Fountain Of Youth'

    def buff(self, target_character):
        if 'animal' in target_character.tribes:
            target_character.bonus_attack += 1
            target_character.bonus_health += 1

            if 'evil' in target_character.tribes:
                target_character.remove('evil')
            elif 'good' in target_character.tribes:
                target_character.append('good')