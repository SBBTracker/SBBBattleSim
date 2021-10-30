from sbbbattlesim.characters import Character


class CharacterType(Character):
    display_name = 'Good Witch of the North'
    support = True

    def buff(self, target_character):
        if 'good' in target_character.tribes:
            target_character.attack_bonus += 4 if self.golden else 2
            target_character.health_bonus += 6 if self.golden else 3

