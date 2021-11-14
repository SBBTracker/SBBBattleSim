from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
import sbbbattlesim
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Princess Peep'
    last_breath = True

    _attack = 1
    _health = 1
    _level = 3
    _tribes = {Tribe.GOOD, Tribe.PRINCESS}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.PrincessPeepDeath)

    class PrincessPeepDeath(OnDeath):
        last_breath = True
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.priority = sbbbattlesim.SUMMONING_PRIORITY

        def handle(self, *args, **kwargs):
            stat = 2 if self.manager.golden else 1

            sheep = []
            for _ in range(3):
                sheep.append(character_registry['Sheep'](
                    owner=self.manager.owner,
                    position=self.manager.position,
                    attack=stat,
                    health=stat,
                    golden=False,
                    keywords=[],
                    tribes=['good', 'animal'],
                    cost=1
                ))

            self.manager.owner.summon(self.manager.position, *sheep)
