import sbbbattlesim
from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe


class ThreeBigPigsDeath(OnDeath):
    last_breath = True

    def handle(self, stack, reason, *args, **kwargs):
        stat = 6 if self.manager.golden else 3

        sheep = [
            character_registry['SBB_CHARACTER_PIGGY'](
                player=self.manager.player,
                position=self.manager.position,
                attack=stat,
                health=stat,
                golden=False,
                keywords=[],
                tribes=['evil', 'animal'],
                cost=1
            ) for _ in range(3)
        ]

        self.manager.player.summon(self.manager.position, sheep)


class CharacterType(Character):
    display_name = 'Three Big Pigs'
    last_breath = True

    _attack = 9
    _health = 9
    _level = 5
    _tribes = {Tribe.EVIL, Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(ThreeBigPigsDeath)
