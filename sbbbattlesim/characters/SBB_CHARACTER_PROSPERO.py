from sbbbattlesim.action import Buff, Aura, Action, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSummon, OnSpawn, OnDespawn

from sbbbattlesim.utils import Tribe


class BearstineOnSummon(OnSummon):
    def handle(self, summoned_characters, stack, *args, **kwargs):
        for char in summoned_characters:
            if char is self.source or Tribe.ANIMAL not in char.tribes:
                continue

            previous_bearstine_buffs = [stat_change for stat_change in char._action_history if stat_change.reason == ActionReason.BEARSTINE_BUFF]
            previous_bearstine_health_buffs = sum(stat_change.health for stat_change in previous_bearstine_buffs)
            previous_bearstine_attack_buffs = sum(stat_change.attack for stat_change in previous_bearstine_buffs)

            stat_multplier = 2 if self.source.golden else 1
            attack_buff = (char.attack - previous_bearstine_attack_buffs) * stat_multplier
            health_buff = (char.health - previous_bearstine_health_buffs) * stat_multplier

            Buff(reason=ActionReason.BEARSTINE_BUFF, source=self.source, targets=[char],
                 attack=attack_buff, health=health_buff, temp=False, stack=stack).resolve()


class BearstineOnDespawn(OnDespawn):
    def handle(self, stack, *args, **kwargs):
        self.source.player.unregister(self.source.buff_event)


class CharacterType(Character):
    display_name = 'Bearstine'
    aura = True

    _attack = 7
    _health = 10
    _level = 6
    _tribes = {Tribe.ANIMAL, Tribe.GOOD, Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        modifier = 4 if self.golden else 2
        self.aura = Aura(source=self, attack=modifier, health=modifier, _lambda=lambda char: Tribe.ANIMAL in char.tribes and char is not self, priority=-20)
        self.buff_event = self.player.register(BearstineOnSummon, source=self, priority=-20)
        self.register(BearstineOnDespawn)
