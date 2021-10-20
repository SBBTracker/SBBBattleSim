from events import LastBreathEvent
from characters import Character
from characters import registry as character_registry

class CharacterType(Character):
    name = 'Princess Peep'

    class PrincessPeepDeath(LastBreathEvent):
        def __call__(self, **kwargs):
            self.character.owner.summon(self.character.position, *[character_registry['Sheep'](1, 1) for _ in range(3)])

    death = [
        PrincessPeepDeath,
    ]
