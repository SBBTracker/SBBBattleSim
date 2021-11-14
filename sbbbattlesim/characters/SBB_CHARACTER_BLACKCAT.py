import sbbbattlesim
from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Black Cat'
    last_breath = True

    _attack = 1
    _health = 1
    _level = 2
    _tribes = {Tribe.EVIL, Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.BlackCatLastBreath)

    class BlackCatLastBreath(OnDeath):
        last_breath = True
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.priority = sbbbattlesim.SUMMONING_PRIORITY

        def handle(self, *args, **kwargs):
            stat = 2 if self.manager.golden else 1
            cats = [character_registry['Cat'](self.manager.owner, self.manager.position, stat, stat, golden=False, keywords=[], tribes=['evil', 'animal'], cost=1)]
            self.manager.owner.summon(self.manager.position, *cats)
            return 'OnLastBreath', [cats], {}
