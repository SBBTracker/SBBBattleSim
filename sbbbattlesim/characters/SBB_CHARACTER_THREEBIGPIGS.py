import sbbbattlesim
from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Three Big Pigs'
    last_breath = True

    _attack = 15
    _health = 15
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.ThreeBigPigsDeath)

    class ThreeBigPigsDeath(OnDeath):
        last_breath = True
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.priority = sbbbattlesim.SUMMONING_PRIORITY

        def handle(self, *args, **kwargs):
            stat = 10 if self.manager.golden else 5

            sheep = [
                character_registry['Pig'](
                    owner=self.manager.owner,
                    position=self.manager.position,
                    attack=stat,
                    health=stat,
                    golden=False,
                    keywords=[],
                    tribes=['evil', 'animal'],
                    cost=1
                ) for _ in range(3)
            ]

            self.manager.owner.summon(self.manager.position, sheep)
