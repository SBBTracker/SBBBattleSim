from sbbbattlesim.events import SlayEvent
from sbbbattlesim.characters import Character


class CharacterType(Character):
    name = 'Vain-Pire'

    class VainPireSlay(SlayEvent):
        def __call__(self, **kwargs):
            amount = 2 if self.character.golden else 1
            self.character.base_attack += amount
            self.character.base_health += amount

    slay = [
        VainPireSlay
    ]


