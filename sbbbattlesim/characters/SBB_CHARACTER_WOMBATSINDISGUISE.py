import random

from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath, OnSummon
from sbbbattlesim.utils import StatChangeCause, Tribe


class WombatsInDisguiseOnSummon(OnSummon):

    def handle(self, summoned_characters, stack, *args, **kwargs):

        attack_buff = self.wombat.attack * (2 if self.wombat.golden else 1)
        health_buff = self.wombat.max_health * (2 if self.wombat.golden else 1)

        for char in summoned_characters:
            if char is self.summon:
                char.change_stats(
                    reason=StatChangeCause.WOMBATS_IN_DISGUISE_BUFF,
                    attack=attack_buff, health=health_buff, temp=False, source=self.wombat
                )


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

            summon.owner.register(WombatsInDisguiseOnSummon, wombat=self.manager, summon=summon)
            self.manager.owner.summon(self.manager.position, [summon])


class CharacterType(Character):
    display_name = 'Wombats In Disguise'

    _attack = 4
    _health = 4
    _level = 5
    _tribes = {Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(WombatsInDisguiseOnDeath, priority=410)  # faster than coin of charon
