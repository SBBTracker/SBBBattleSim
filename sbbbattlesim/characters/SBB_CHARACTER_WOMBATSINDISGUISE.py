import random

from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import StatChangeCause, Tribe


class WombatsInDisguiseOnDeath(OnDeath):
    last_breath = True

    def handle(self, stack, *args, **kwargs):
        _lambda = lambda char: char._level <= self.manager.owner.level
        valid_summons = [*character_registry.filter(_lambda=_lambda)]

        if valid_summons:
            summon = random.choice(valid_summons).new(
                owner=self.manager.owner,
                position=self.manager.position,
                golden=self.manager.golden
            )

            attack_buff = self.manager.attack * (2 if self.manager.golden else 1)
            health_buff = self.manager.health * (2 if self.manager.golden else 1)

            summon.change_stats(
                attack=attack_buff, health=health_buff,
                reason=StatChangeCause.WOMBATS_IN_DISGUISE_BUFF, source=self.manager,
                stack=stack
            )

            self.manager.owner.summon(self.manager.position, [summon])


class CharacterType(Character):
    display_name = 'Wombats In Disguise'

    _attack = 4
    _health = 4
    _level = 5
    _tribes = {Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(WombatsInDisguiseOnDeath)
