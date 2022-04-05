from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe


class PapaBearOnDeath(OnDeath):
    last_breath = True

    def handle(self, stack, reason, *args, **kwargs):
        stat = 8 if self.manager.golden else 4
        mama = character_registry['SBB_CHARACTER_MAMABEAR'](
            player=self.manager.player,
            position=self.manager.position,
            attack=stat,
            health=stat,
            golden=False,
            tribes=[Tribe.GOOD, Tribe.ANIMAL],
            cost=1
        )
        self.manager.player.summon(self.manager.position, [mama])


class CharacterType(Character):
    display_name = 'Papa Bear'
    last_breath = True

    _attack = 4
    _health = 4
    _level = 1
    _tribes = {Tribe.ANIMAL, Tribe.GOOD}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(PapaBearOnDeath)
