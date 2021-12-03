from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath, OnSummon
import random

from sbbbattlesim.utils import Tribe, StatChangeCause


class CharacterType(Character):
    display_name = 'Bearstine'

    aura = True

    _attack = 7
    _health = 10
    _level = 6
    _tribes = {Tribe.ANIMAL, Tribe.GOOD}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class BearstineOnSummon(OnSummon):
            bearstine = self
            def handle(self, summoned_characters, stack, *args, **kwargs):
                for char in summoned_characters:
                    if Tribe.ANIMAL not in char.tribes:
                        continue

                    stat_multplier = 2 if self.bearstine.golden else 1

                    previous_bearstine_buffs = [stat_change for stat_change in char.stat_history if stat_change.reason == StatChangeCause.BEARSTINE_BUFF]
                    previous_bearstine_attack_buffs = sum(stat_change.attack for stat_change in previous_bearstine_buffs)
                    if "SBB_TREASURE_WHIRLINGBLADES" in self.manager.treasures:
                        if '''SBB_TREASURE_TREASURECHEST''' in self.manager.treasures:
                            previous_bearstine_attack_buffs *= 3
                        else:
                            previous_bearstine_attack_buffs *= 2

                    previous_bearstine_health_buffs = sum(stat_change.health for stat_change in previous_bearstine_buffs)

                    attack_buff = (char.attack - previous_bearstine_attack_buffs) * stat_multplier
                    health_buff = (char.health - previous_bearstine_health_buffs) * stat_multplier

                    char.change_stats(attack=attack_buff, health=health_buff, reason=StatChangeCause.BEARSTINE_BUFF,
                                      source=self.bearstine, temp=False, stack=stack)

        self.owner.register(BearstineOnSummon)

    def buff(self, target_character, *args, **kwargs):
        if Tribe.ANIMAL in target_character.tribes and target_character != self:
            modifier = 4 if self.golden else 2
            target_character.change_stats(
                attack=modifier, health=modifier, temp=True,
                reason=StatChangeCause.AURA_BUFF, source=self, *args, **kwargs
            )
