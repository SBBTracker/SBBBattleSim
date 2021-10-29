from sbbbattlesim.characters import Character
from sbbbattlesim.events import Slay


class CharacterType(Character):
    name = 'Vain-Pire'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.VainPireSlay)

    class VainPireSlay(Slay):
        def __call__(self, **kwargs):
            amount = 2 if self.character.golden else 1
            self.character.base_attack += amount
            self.character.base_health += amount
