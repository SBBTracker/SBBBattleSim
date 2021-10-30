from sbbbattlesim.characters import Character


class CharacterType(Character):
    display_name = 'Good Witch of the North'
    support = True

    def buff(self, target_character):
        if 'good' in target_character.tribes:
            golden_multiplyer = 2 if self.golden else 1
            target_character.change_stats(attack=2*golden_multiplyer, health=3*golden_multiplyer, temp=True, reason=f'Support from {self}')
