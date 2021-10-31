from sbbbattlesim.characters import Character


class CharacterType(Character):
    display_name = 'Wicked Witch of the West'
    support = True

    def buff(self, target_character):
        if 'evil' in target_character.tribes:
            golden_multiplyer = 2 if self.golden else 1
            target_character.change_stats(attack=3*golden_multiplyer, health=2*golden_multiplyer, temp=True, reason=f'Support from {self}')
