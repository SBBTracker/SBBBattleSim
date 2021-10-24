from sbbbattlesim.characters import Character


class CharacterType(Character):
    name = 'Mad Mim'
    support = True

    def buff(self, target_character):
        target_character.attack_bonus += 6 if self.golden else 3
