import sbbbattlesim
from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe


class PrincessPeepDeath(OnDeath):
    last_breath = True

    def handle(self, stack, reason, *args, **kwargs):
        stat = 2 if self.source.golden else 1

        sheep = [
            character_registry['SBB_CHARACTER_SHEEP'](
                player=self.source.player,
                position=self.source.position,
                attack=stat,
                health=stat,
                golden=False,
                keywords=[],
                tribes=['good', 'animal'],
                cost=1
            ) for _ in range(3)
        ]

        self.manager.player.summon(self.manager.position, sheep)


class CharacterType(Character):
    display_name = 'Princess Peep'
    last_breath = True

    _attack = 1
    _health = 1
    _level = 3
    _tribes = {Tribe.GOOD, Tribe.ROYAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(PrincessPeepDeath)
