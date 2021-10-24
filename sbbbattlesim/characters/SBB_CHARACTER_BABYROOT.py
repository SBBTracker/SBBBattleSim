from sbbbattlesim.events import BuffsEvent
from sbbbattlesim.characters import Character



class CharacterType(Character):
    name = 'Baby Root'
    support = True

    def buff(self, target_character):
        target_character.health_bonus += 6 if self.golden else 3
