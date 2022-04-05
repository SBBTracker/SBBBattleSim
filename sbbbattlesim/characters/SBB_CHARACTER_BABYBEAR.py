from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe


class BabyBearOnDeath(OnDeath):
    last_breath = True

    def handle(self, stack, reason, *args, **kwargs):
        stat = 4 if self.manager.golden else 2
        papa_bear = character_registry['SBB_CHARACTER_PAPABEAR'](
            player=self.manager.player,
            position=self.manager.position,
            health=stat,
            attack=stat,
            golden=self.manager.golden,
            tribes=[Tribe.GOOD, Tribe.ANIMAL],
            cost=1
        )
        self.manager.player.summon(self.manager.position, [papa_bear])


class CharacterType(Character):
    display_name = 'Baby Bear'
    last_breath = True

    _attack = 2
    _health = 2
    _level = 5
    _tribes = {Tribe.GOOD, Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(BabyBearOnDeath)
