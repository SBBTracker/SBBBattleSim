from sbbbattlesim.characters import Character


class BuffEvent(object):
    pass


class CharacterType(Character):
    name = 'Labyrinth Minotaur'
    aura = True

    def buff(self, target_character):
        if 'evil' in target_character.tribes and target_character != self:
            target_character.attack_bonus += 1
