from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath


class CharacterType(Character):
    name = 'Wretched Mummy'

    class WretchedMummyDeath(OnDeath):
        def handle(self, dead_thing, *args, **kwargs):
            damage = 8 if self.manager.golden else 4
            for char in kwargs['defender'].characters.values():
                char.damage += damage
            return 'OnLastBreath', [], {'damage_done': damage}

    events = (
        WretchedMummyDeath,
    )
