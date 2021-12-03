from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath, OnSummon
import sbbbattlesim
from sbbbattlesim.characters import registry as character_registry

import random

from sbbbattlesim.utils import Tribe, StatChangeCause

JULIET_ID = 'SBB_CHARACTER_JULIET'

class CharacterType(Character):
    display_name = 'Romeo'
    last_breath = True

    _attack = 5
    _health = 3
    _level = 3
    _tribes = {Tribe.GOOD, Tribe.PRINCE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class RomeoLastBreath(OnDeath):
            last_breath = True
            romeo = self

            def handle(self, *args, **kwargs):
                dead_juliets = [j for j in self.manager.owner.graveyard if j.id == JULIET_ID]

                if dead_juliets:
                    juliet = max(dead_juliets, key=lambda juliet: (juliet.attack, juliet.health))
                    juliet._damage = 0

                    new_juliet = character_registry[juliet.id](
                        attack=juliet._base_attack,
                        health=min(juliet._base_health, 1),
                        tribes=juliet.tribes,
                        golden=juliet.golden,
                        position=self.romeo.position,
                        cost=juliet.cost,
                        owner=juliet.owner,
                    )
                    self.juliet = new_juliet

                    class RomeoOnSummon(OnSummon):
                        juliet = self.juliet
                        romeo = self.romeo
                        triggered = False

                        def handle(self, summoned_characters, stack, *args, **kwargs):
                            if self.triggered:
                                return
                            self.triggered = True
                            for char in summoned_characters:
                                if char is self.juliet:
                                    modifier = 14 if self.romeo.golden else 7
                                    char.change_stats(
                                        reason=StatChangeCause.ROMEO_BUFF, attack=modifier,
                                        health=modifier, temp=False, source=self.romeo
                                    )

                    self.manager.owner.register(RomeoOnSummon)
                    self.manager.owner.summon(self.manager.position, [new_juliet])


        self.register(RomeoLastBreath)

