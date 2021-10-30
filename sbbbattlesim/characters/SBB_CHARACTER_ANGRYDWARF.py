from sbbbattlesim.characters import Character


class CharacterType(Character):
    display_name = 'Fanny'
    support = True

    def buff(self, target_character):
        if 'dwarf' in target_character.tribes:
            target_character.attack_bonus += 4 if self.golden else 2
            target_character.health_bonus += 4 if self.golden else 2
