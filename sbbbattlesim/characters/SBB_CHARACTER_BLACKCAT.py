from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath


class CharacterType(Character):
    name = 'Black Cat'

    class BlackCatLastBreath(OnDeath):
        def handle(self, dead_thing, *args, **kwargs):
            stat = 2 if self.manager.golden else 1
            cats = [character_registry['Cat'](self.manager.owner, self.manager.position, stat, stat, golden=False, keywords=[], tribes=['evil', 'animal'])]
            self.manager.owner.summon(self.manager.position, *cats)
            return 'OnLastBreath', [cats], {}

    events = (
        BlackCatLastBreath,
    )
