from events import SlayEvent
from characters import Character


class CharacterType(Character):
    name = 'Vain-Pire'

    class VainPireSlay(SlayEvent):
        def __call__(self, **kwargs):
            self.character.base_attack += 1
            self.character.base_health += 1

    slay = [
        VainPireSlay
    ]


