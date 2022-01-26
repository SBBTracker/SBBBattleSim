import random

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe


class WombatsInDisguiseOnDeath(OnDeath):
    last_breath = True

    def handle(self, stack, reason, *args, **kwargs):
        _lambda = lambda char: char._level <= self.manager.player.level and char.id != "SBB_CHARACTER_WOMBATSINDISGUISE"
        valid_summons = [*character_registry.filter(_lambda=_lambda)]

        if valid_summons:
            summon = random.choice(valid_summons).new(
                player=self.manager.player,
                position=self.manager.position,
                golden=self.manager.golden
            )

            attack_buff = self.source.attack * (2 if self.source.golden else 1)
            health_buff = self.source.max_health * (2 if self.source.golden else 1)

            Buff(reason=ActionReason.WOMBATS_IN_DISGUISE_BUFF, source=self.source,
                 attack=attack_buff, health=health_buff, temp=False).execute(summon)

            self.manager.player.summon(self.manager.position, [summon])


class CharacterType(Character):
    display_name = 'Wombats In Disguise'

    _attack = 4
    _health = 4
    _level = 5
    _tribes = {Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(WombatsInDisguiseOnDeath, priority=410)  # faster than coin of charon
