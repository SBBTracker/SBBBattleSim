import sbbbattlesim
from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Baby Bear'
    last_breath = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.BabyBearLastBreath)


    class BabyBearLastBreath(OnDeath):
        last_breath = True
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.priority = sbbbattlesim.SUMMONING_PRIORITY

        def handle(self, *args, **kwargs):
            stat = 4 if self.manager.golden else 2
            papa_bear = PapaBear(owner=self.manager.owner,
                                 position=self.manager.position,
                                 health=stat,
                                 attack=stat,
                                 golden=self.manager.golden,
                                 keywords=[],
                                 tribes=[Tribe.GOOD, Tribe.ANIMAL],
                                 cost=1
                                 )
            self.manager.owner.summon(self.manager.position, papa_bear)
            return 'OnLastBreath', [papa_bear], {}

# Instantiate Papa Bear
class PapaBear(Character):
    display_name = 'Papa Bear'
    last_breath = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.golden_base = self.golden
        self.golden = False

        self.register(self.PapaBearLastBreath)

    class PapaBearLastBreath(OnDeath):
        last_breath = True
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.priority = sbbbattlesim.SUMMONING_PRIORITY

        def handle(self, *args, **kwargs):
            stat = 8 if self.manager.golden_base else 4
            mama = character_registry['Mama Bear'](self.manager.owner, self.manager.position, stat, stat,
                                                   golden=False, keywords=[], tribes=['good', 'animal'], cost=1)

            self.manager.owner.summon(self.manager.position, mama)
            return 'OnLastBreath', [mama], {}
