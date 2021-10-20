from events import LastBreathEvent
from characters import Character
from characters import registry as character_registry


class CharacterType(Character):
    name = 'Black Cat'

    class BlackCatDeath(LastBreathEvent):
        def __call__(self, **kwargs):
            self.character.owner.summon(self.character.position, character_registry['Cat'](1, 1))

    death = [
        BlackCatDeath,
    ]
