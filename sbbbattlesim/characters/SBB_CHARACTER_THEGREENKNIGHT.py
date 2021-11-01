from sbbbattlesim.characters import Character


class CharacterType(Character):
    display_name = 'The Green Knight'
    support = True

    def buff(self, target_character):
        target_character.change_stats(health=20 if self.golden else 10, reason=f'{self} support', temp=True)
