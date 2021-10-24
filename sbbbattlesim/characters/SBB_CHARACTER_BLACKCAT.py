from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import Death


class CharacterType(Character):
    name = 'Black Cat'

    class BlackCatLastBreath(Death):
        def __call__(self, **kwargs):
            stat = 2 if self.character.golden else 1
            self.character.owner.summon(self.character.position, character_registry['Cat'](stat, stat))

    events = (
        BlackCatLastBreath,
    )
