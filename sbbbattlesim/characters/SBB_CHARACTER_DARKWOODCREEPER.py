from sbbbattlesim.characters import Character
from sbbbattlesim.events import DamagedAndSurvived


class DarkwoodCreeperOnDamage(DamagedAndSurvived):
    def __call__(self, **kwargs):
        self.character.attack += 2 if self.character.golden else 1


class CharacterType(Character):
    name = 'Darkwood Creeper'

    def buff(self, target_character):
        target_character.register(DarkwoodCreeperOnDamage, temp=True)
