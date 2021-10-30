from sbbbattlesim.characters import Character


class CharacterType(Character):
    display_name = 'Rainbow Unicorn'
    aura = True

    def buff(self, target_character):
        if 'good' in target_character.tribes and target_character != self:
            target_character.change_stats(health=2 if self.golden else 1, temp=True, reason=f'{self} health aura')
