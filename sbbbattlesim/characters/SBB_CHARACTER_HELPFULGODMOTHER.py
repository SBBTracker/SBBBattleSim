from sbbbattlesim.characters import Character


class CharacterType(Character):
    display_name = 'Rainbow Unicorn'
    aura = True

    def buff(self, target_character):
        if 'good' in target_character.tribes and target_character != self:
            target_character.health_bonus += 1
