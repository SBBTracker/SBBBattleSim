from sbbbattlesim.characters import Character
from sbbbattlesim.events import DamagedAndSurvived, Death


class DarkwoodCreeperOnDamage(DamagedAndSurvived):
    def __call__(self, **kwargs):
        self.character.attack += 2 if self.character.golden else 1


class DarkwoodCreeperDeath(Death):
    def __call__(self, **kwargs):
        for char in self.character.owner.characters.values():
            if char is not None:
                char.unregister(DarkwoodCreeperOnDamage)


class CharacterType(Character):
    name = 'Darkwood Creeper'

    def buff(self, target_character):
        target_character.register(DarkwoodCreeperOnDamage)

    events = (
        DarkwoodCreeperDeath,
    )
