import sbbbattlesim
from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe


class PrincessPeepDeath(OnDeath):
    last_breath = True

    def handle(self, *args, **kwargs):
        stat = 2 if self.manager.golden else 1

        sheep = [
            character_registry['SBB_CHARACTER_SHEEP'](
                owner=self.manager.owner,
                position=self.manager.position,
                attack=stat,
                health=stat,
                golden=False,
                keywords=[],
                tribes=['good', 'animal'],
                cost=1
            ) for _ in range(3)
        ]

        self.manager.owner.summon(self.manager.position, sheep)


class CharacterType(Character):
    display_name = 'Princess Peep'
    last_breath = True

    _attack = 1
    _health = 1
    _level = 3
    _tribes = {Tribe.GOOD, Tribe.PRINCESS}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(PrincessPeepDeath, priority=sbbbattlesim.SUMMONING_PRIORITY)
