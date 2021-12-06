from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe


class PapaBearOnDeath(OnDeath):
    last_breath = True

    def handle(self, *args, **kwargs):
        stat = 8 if self.manager.golden else 4
        mama = character_registry['SBB_CHARACTER_MAMABEAR'](
            owner=self.manager.owner,
            position=self.manager.position,
            attack=stat,
            health=stat,
            golden=False,
            tribes=[Tribe.GOOD, Tribe.ANIMAL],
            cost=1
        )
        self.manager.owner.summon(self.manager.position, [mama])


class CharacterType(Character):
    display_name = 'Papa Bear'
    last_breath = True

    _attack = 2
    _health = 2
    _level = 1
    _tribes = {Tribe.ANIMAL, Tribe.GOOD}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(PapaBearOnDeath)