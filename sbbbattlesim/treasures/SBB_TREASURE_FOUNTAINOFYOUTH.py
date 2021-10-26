from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    name = 'Fountain Of Youth'

    def buff(self, target_character):
        target_character.bonus_health += 1