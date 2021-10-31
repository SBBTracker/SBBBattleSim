from sbbbattlesim.characters import Character


class CharacterType(Character):
    display_name = 'Baby Root'
    support = True

    def buff(self, target_character):
        target_character.change_stats(health=6 if self.golden else 3, reason=f'{self} support', temp=True)
