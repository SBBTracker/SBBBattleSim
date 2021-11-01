from sbbbattlesim.characters import Character


class CharacterType(Character):
    display_name = 'Grumble Gore'
    support = True

    def buff(self, target_character):
        target_character.change_stats(attack=20 if self.golden else 10, temp=True, reason=f'{self} support buff')
